---
layout:     post

title:      transformer详解

date:       2025-02-10

author:     phoenixZ

header-img: img/oip2.jpg

catalog: true

tags:

    - 大模型
    - transformer
---

# 一 整体框架

![]({{ site.baseurl }}/img/transformer整体结构.png)
![]({{ site.baseurl }}/img/transformer-编解码器.png)

编码器： 把输入变成词向量(self-attention)
解码器： 把词向量变成输出(self-attention + cross-attention)



# 二 Encoder结构

## 编码器详解

![]({{ site.baseurl }}/img/Transformer_encoder.png)

**每一个子层的传输过程中都加入了残差连接和归一化**    

![]({{ site.baseurl }}/img/transformer-encoder1.png)
1. 根据上图 ， thinking-> 得到X1（词向量， 可以通过one-hot、 word2vec、 glove、bert等方法得到）
2. 叠加位置编码，赋予位置关系
3. 然后X1经过self-attention层，得到Z1 （x1 与 x1,x2拼接起来的句子做的自注意力机制的词向量， 具备语义特征和位置特征）
4. 残差网络（避免梯度消失）
   - 通过跳跃连接（skip connection）直接将输入加到输出上：`output = F(x) + x`
   - 反向传播时，梯度可以直接通过跳跃连接传递，不会衰减
   - 保证了至少有一条梯度为1的路径，避免了梯度消失

5. 归一化（避免梯度爆炸）
   - 使用Layer Normalization将数据归一化到均值为0，方差为1
   - 计算公式：`y = γ * (x - μ) / (σ + ε) + β`
     - μ: 均值
     - σ: 标准差
     - γ, β: 可学习的缩放和偏移参数
     - ε: 很小的常数，防止除0
   - 通过控制数据分布在合理范围内，避免激活值过大导致梯度爆炸
6. Feed Forward 
   - 该层负责对每个位置的表示进行独立的线性变换，通常包含两个线性变换和一个激活函数（如ReLU）。
   - 计算公式为：`FFN(x) = max(0, xW_1 + b_1)W_2 + b_2`
     - 其中，`W_1`和`W_2`是可学习的权重矩阵，`b_1`和`b_2`是偏置项。
   - 通过这种方式，Feed Forward层能够为每个位置的表示引入非线性特征，从而增强模型的表达能力。

  💡 **4和5的详细解释**

  - **残差网络避免梯度消失：**  
    1. 在深层网络中，多层传递会导致梯度逐层衰减。
    2. 残差连接提供了一条直接的梯度传递通道，即使其他路径的梯度接近0，这条直接通道也能保证梯度至少为1。
    3. 这样即使网络很深，梯度也能有效地传递到浅层。

  - **Layer Normalization避免梯度爆炸：**  
    1. 神经网络中的数据分布可能会随着层数加深而发生偏移和扩大。
    2. Layer Normalization通过归一化保持每一层的数据分布稳定，将数据约束在合理范围内，避免激活值过大。
    3. 可学习的参数γ和β允许模型自适应调整归一化的程度。
    4. 稳定的数据分布有助于梯度保持在合理范围内，防止爆炸。

## 位置编码演变历程

### 整型标记位置

给第一个token标记1，第二个标记2，以此类推这样做的问题是 👇

1. 模型如果遇见比训练时更长的序列， 泛化能力不好
2. 模型的位置表示可能无界

### [0,1]范围标记位置

0表示第一个位置，1表示最后一个位置，这样做的问题是 👇

大部分序列长度不同时，token间的相对距离不一样了

### 💡 因此，位置表示方式需要满足

1. 能表示token在序列中的绝对位置
2. 能表示token之间的相对距离
3. 不同长度序列中相同相对距离的token对应的位置编码应该相似
4. 位置编码的取值应该有界

## 位置编码

🍎 位置表示公式:
$$
PE_{(pos,2i)} = sin(pos/10000^{2i/d_{model}})     \tag{1}
$$

其中：

- pos: 表示token在序列中的位置（从0开始的索引）
- i: 表示维度对的索引（从0到d_model/2-1）
- d_model: 表示模型的隐藏层维度大小

$$
PE_{(pos,2i+1)} = cos(pos/10000^{2i/d_{model}})   \tag{2}
$$

举例说明：

- 如果d_model=512，那么i的取值范围是[0,255]
- **每个token的位置编码都是一个d_model维的向量**
- 偶数维度(2i)使用sin函数，奇数维度(2i+1)使用cos函数
- 10000的指数项使得不同维度有不同的波长，形成多尺度的位置表示

🍊 余弦定理

$$
sin(α+β) = sin(α)cos(β) + cos(α)sin(β)     \tag{3}
$$

$$
cos(α+β) = cos(α)cos(β) - sin(α)sin(β)     \tag{4}
$$

🍌 由公式1，2，3，4，可以推导出：

$$
PE_{(pos+k,2i)} = sin(pos/10000^{2i/d_{model}})cos(k/10000^{2i/d_{model}}) + cos(pos/10000^{2i/d_{model}})sin(k/10000^{2i/d_{model}})
$$

$$
PE_{(pos+k,2i+1)} = cos(pos/10000^{2i/d_{model}})cos(k/10000^{2i/d_{model}}) - sin(pos/10000^{2i/d_{model}})sin(k/10000^{2i/d_{model}})
$$

**由此可以看出，位置编码的点积可以表示相对位置信息，从而可以表示token之间的相对距离。**



# 三 Decoder 结构

![]({{ site.baseurl }}/img/transformer-decoder.png)

**解码器接收编码器生成的词向量，然后生成翻译的结果。**

## 结构解释

在训练阶段，目标词语 **"我是一个学生"** 是已知的，因此需要使用 **mask** 来限制 **self-attention** 的计算。这样做的目的是确保解码器在生成每个词时，只能依赖于当前及之前的词，而不能看到未来的词。例如：

- **第一次**：self-attention 只对 **"我"** 进行计算
- **第二次**：self-attention 对 **"我"** 和 **"是"** 进行计算

> 通过这种方式，模型能够更好地模拟实际的生成过程，避免在训练阶段获得全部信息，从而提高模型的泛化能力和预测准确性。

解码器中的两个自注意力机制分别用于不同的阶段：

1. **掩码自注意力机制（Masked Self-Attention）**：
   - **用途**：为了防止模型在生成当前词时看到未来的词，掩码自注意力机制会在计算注意力权重时对未来的词进行屏蔽。这确保了模型只能依赖于当前及之前的词进行生成，模拟了实际的生成过程。
   - **阶段**：此机制在训练阶段的每个时间步都被使用，确保模型在生成时遵循因果关系。
   - **公式**：掩码自注意力的计算可以表示为：
   
   $$
   \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V
   $$


2. **自注意力机制（Self-Attention）**：
   - **用途**：在解码器的每个时间步，当前的词（或 token）会通过自注意力机制与之前生成的所有词进行交互，以捕捉上下文信息。这使得模型能够在生成当前词时，考虑到之前生成的词，从而提高生成的连贯性和上下文相关性。
   - **阶段**：此机制在解码器的每个时间步都被使用，确保生成的每个词都能基于之前的词进行调整。
   - **公式**：自注意力的计算可以表示为：
   
   $$
   \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
   $$

3. **线性变换和激活函数**：
   - 解码器将通过一个线性层对自注意力机制的输出进行变换，通常会使用 ReLU 激活函数来引入非线性。
   - **公式**：线性变换可以表示为：
   
   $$
   Y = WX + b
   $$


4. **添加和归一化**：
   - 将自注意力的输出与输入进行残差连接（Add），然后进行层归一化（Layer Normalization），以稳定训练过程。
   - **公式**：残差连接可以表示为：
   
   $$
   \text{Output} = \text{LayerNorm}(X + \text{Attention}(Q, K, V))
   $$

5. **前馈神经网络**：
   - 解码器的输出会传递到一个前馈神经网络（Feed Forward Neural Network），该网络通常由两个线性层和一个激活函数（如 ReLU）组成。
   - **公式**：前馈网络的计算可以表示为：
   
   $$
   \text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2
   $$

6. **再次添加和归一化**：
   - 前馈网络的输出同样会进行残差连接和层归一化。
   - **公式**：再次的残差连接可以表示为：
   
   $$
   \text{Output} = \text{LayerNorm}(X + \text{FFN}(X))
   $$

7. **输出生成**：
   - 最后，解码器的输出会通过一个线性层映射到词汇表的维度，并使用 softmax 函数生成每个词的概率分布，从而预测下一个词。
   - **公式**：输出生成可以表示为：
   
   $$
   P(\text{next word}) = \text{softmax}(YW + b)
   $$

> 通过这些步骤，解码器能够有效地生成符合上下文的输出，确保生成的每个词都能基于之前的词进行调整，从而提高生成的连贯性和上下文相关性。


## 总结

我的理解是：

1. **训练阶段**：利用掩码自注意力（Masked Self-Attention），这样做是为了避免获取到全部信息，从而提升模型的泛化能力。

2. **预测阶段**：编码器输出键（k）和值（v），解码器结合自身输入查询（Q），进行自注意力计算。

3. **计算结果**：将计算的结果与输入的Q相加，然后进行归一化。

4. **线性变换**：再进行一次线性变换。

5. **生成概率分布**：最后通过softmax生成每个词的概率分布。

💡 这里使用一层线性变换，是将注意力机制的输出结果映射到不同的特征空间，这样做可以适应模型后续层的需求；第二点是通过激活函数，引入非线性，增强模型的表达能力。









# 四 注意力机制理解

## 注意力机制

### 1. 数据示例

下面的表格展示了 Key 和对应的 Value：

| Key (腰围) | Value (体重) |
|:----------:|:------------:|
| 51         | 40           |
| 56         | 43           |
| 58         | 48           |

### 2. 单值预测问题

- **问题描述：**  
  给定一个人的腰围为 57（query），直观上可能预测体重在 43 到 48 之间。简单的计算思路是：(43 + 48) / 2 = 45.5，进而可以认为腰围为 56 和 58 的样本各占 0.5 的权重（因 57 接近于 56 和 58）。

- **存在问题：**  
  这种方法忽略了所有 Key 和 Value 的信息，没有充分利用可用数据。

### 3. 调整注意力权重

- **目标：**  
  通过引入注意力权重 α(q, kᵢ) 来对所有 Key 进行加权求和，从而提高预测准确性。

- **数学表达：**

$$
f(q) = \alpha(q, k_1)v_1 + \alpha(q, k_2)v_2 + \alpha(q, k_3)v_3 = \sum_{i=1}^{3}\alpha(q, k_i)v_i
$$

- **softmax 处理：**  
  对原始注意力分数应用 softmax，可以将它们转换为归一化的概率分布，既保证了所有 Key 权重之和为 1，又能放大与 query 匹配度高的 Key 的影响，使加权求和输出更能反映各 Key 的重要性。

### 4. 高维向量情况

当处理高维向量时，举例说明如下：

<div align="center">
  <table>
    <tr>
      <th>矩阵Q</th>
      <th>矩阵K</th>
      <th>矩阵V</th>
    </tr>
    <tr>
      <td>
        <table>
          <tr>
            <th>col1</th>
            <th>col2</th>
          </tr>
          <tr>
            <td>57</td>
            <td>83</td>
          </tr>
          <tr>
            <td>76</td>
            <td>55</td>
          </tr>
        </table>
      </td>
      <td>
        <table>
          <tr>
            <th>col1</th>
            <th>col2</th>
          </tr>
          <tr>
            <td>51</td>
            <td>70</td>
          </tr>
          <tr>
            <td>58</td>
            <td>88</td>
          </tr>
          <tr>
            <td>56</td>
            <td>82</td>
          </tr>
        </table>
      </td>
      <td>
        <table>
          <tr>
            <th>col1</th>
            <th>col2</th>
          </tr>
          <tr>
            <td>40</td>
            <td>55</td>
          </tr>
          <tr>
            <td>43</td>
            <td>59</td>
          </tr>
          <tr>
            <td>48</td>
            <td>65</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</div>

- **矩阵表达：**

$$
f(Q) = softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

- **为何除以 √dₖ？**
  - 当 dₖ 较大时, QK^T 的值会变得非常大，使得 softmax 函数的输出趋向于 1, 从而可能导致梯度消失问题。
  - 除以 √dₖ 能将 QK^T 的值缩放到合理范围，确保 softmax 输出稳定。

## 自注意力机制简介

- **定义：**  
  自注意力机制中,Query (Q)、Key (K) 和 Value (V) 都是从同一输入 X 中生成（通常是字向量加位置编码）。

- **线性变换：**

$$
Q = XW_Q,\quad K = XW_K,\quad V = XW_V
$$

其中, W₍Q₎、W₍K₎ 和 W₍V₎ 是可学习的参数矩阵。


# 五 示例

![]({{ site.baseurl }}/img/tf-动态结果-2.gif)



##  输入处理阶段
1. **分词**：
   - 输入句子被分割成单词或子词
   - 例如："I am a student" → ["I", "am", "a", "student"]

2. **词嵌入**：
   - 每个词转换为固定维度的向量（如512维）
   - 添加位置编码，注入位置信息

##  编码器处理
1. **Self-Attention计算**：
   - 每个词与句子中所有词计算注意力分数
   - 例如："student"这个词会与"I"、"am"、"a"、"student"都计算关联度

2. **多头注意力**：
   - 并行执行多组注意力计算（通常8个头）
   - 每个头关注不同的特征模式
   - 最后将多个头的结果合并

3. **前馈网络处理**：
   - 对每个位置独立进行特征转换
   - 增强表示能力

## 解码器处理
1. **掩码自注意力**：
   - 生成第一个词时，只能看到开始符号
   - 生成第二个词时，能看到第一个词
   - 依此类推

2. **编码器-解码器注意力**：
   - 解码器的每个词都会关注编码器的完整输出
   - 建立源语言和目标语言的对应关系

3. **输出生成**：
   - 通过softmax层预测每个位置最可能的词
   - 逐个生成翻译结果

## 实际示例
假设翻译 "I am a student" → "我是一个学生"：

1. **第一步**：
   - 输入: ["I", "am", "a", "student"]
   - 解码器首先生成"我"
   - 注意力主要集中在"I"上

2. **第二步**：
   - 已知: "我"
   - 生成: "是"
   - 注意力主要集中在"am"上

3. **第三步**：
   - 已知: "我是"
   - 生成: "一个"
   - 注意力关注"a"

4. **第四步**：
   - 已知: "我是一个"
   - 生成: "学生"
   - 注意力主要集中在"student"上

## 关键特点
1. **并行计算**：
   - 编码器可以并行处理所有输入词
   - 大大提高了计算效率

2. **全局视野**：
   - 每个词都能直接关注到所有其他词
   - 有效捕捉长距离依赖

3. **动态权重**：
   - 注意力权重是动态计算的
   - 能根据上下文自适应调整关注点

4. **双向信息**：
   - 编码器可以双向获取信息
   - 解码器通过掩码实现单向预测




