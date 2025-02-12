# 导入必要的库
import numpy as np  # 用于数值计算
import matplotlib.pyplot as plt  # 用于绘图可视化

def positional_encoding(seq_len, d_model):
    """
    生成位置编码矩阵
    这个函数实现了transformer中的位置编码,用三角函数生成位置向量
    
    Args:
        seq_len: 序列长度,表示输入序列中token的数量
        d_model: 编码维度,表示每个位置向量的维度大小
    Returns:
        pos_encoding: [seq_len, d_model] 的位置编码矩阵,每行代表一个位置的编码向量
    """
    # 创建一个形状为[seq_len, d_model]的零矩阵用于存储位置编码
    pos_encoding = np.zeros((seq_len, d_model))
    
    # positions形状为[seq_len, 1],表示每个位置的索引
    # np.newaxis增加一个维度便于后续广播计算
    positions = np.arange(seq_len)[:, np.newaxis]     # [seq_len, 1]
    
    # 计算不同维度的频率因子
    # np.arange(0, d_model, 2)生成[0,2,4,...,d_model-2]
    # 使用exp和log计算10000^(2i/d_model)的倒数
    div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))  # [d_model/2]
    
    # 使用sin和cos函数计算位置编码
    # 0::2表示偶数维度使用sin
    # 1::2表示奇数维度使用cos 
    pos_encoding[:, 0::2] = np.sin(positions * div_term)  # 偶数维度
    pos_encoding[:, 1::2] = np.cos(positions * div_term)  # 奇数维度
    
    return pos_encoding

if __name__ == "__main__":
    # 生成一个示例位置编码
    seq_length = 100  # 序列长度设为100
    d_model = 512    # 编码维度设为512
    pe = positional_encoding(seq_length, d_model)

    # 使用热力图可视化位置编码矩阵
    plt.figure(figsize=(15, 8))
    plt.pcolormesh(pe, cmap='RdBu')  # RdBu色图可以显示正负值
    plt.xlabel('Dimension')  # x轴表示维度
    plt.ylabel('Position')   # y轴表示位置
    plt.colorbar()          # 添加颜色条
    plt.title("Positional Encoding Visualization")
    plt.show()

    # 验证两个位置向量的点积能反映它们的相对位置关系
    pos1, pos2 = 20, 25  # 选择两个位置
    relative_pos = pos2 - pos1  # 计算相对距离
    similarity = np.dot(pe[pos1], pe[pos2])  # 计算它们编码向量的点积
    print(f"Position {pos1} and {pos2} (relative distance {relative_pos})")
    print(f"Cosine similarity: {similarity}")  # 打印相似度
