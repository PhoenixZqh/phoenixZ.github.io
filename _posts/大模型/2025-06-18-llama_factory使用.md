---
layout:     post
title:      llama_factory使用
date:       2025-06-18
author:     phoenixZ
header-img: img/oip5.jpeg
catalog: true
tags:
    - 大模型
---
1. 下载llama-3-8B-instruct模型

```xml
modelscope download --model LLM-Research/Meta-Llama-3-8B-Instruct
```

2. 

```xml
CUDA_VISIBLE_DEVICES=0 llamafactory-cli webchat     --model_name_or_path /home/datasets/model/LLM-Research/Meta-Llama-3-8B-Instruct
```
