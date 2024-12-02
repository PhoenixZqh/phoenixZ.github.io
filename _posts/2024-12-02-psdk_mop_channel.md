---
layout:     post

title:      PSDK 互联互通

date:       2024-12-02

author:     phoenixZ

header-img: img/dji1.jpg

catalog: true

tags:

    - dji

    - psdk
---
# 一 基本流程

## SDK 互联互通功能初始化

基于 PSDK 开发的负载设备如需使用 SDK 互联互通功能，需要先初始化 SDK 互联互通模块。

```c
T_DjiReturnCode DjiMopChannel_Init(void);
```

## 创建通道

基于 PSDK 开发的负载设备根据用户指定的需求，创建相应的通道类型：可靠传输和不可靠传输。

```c
T_DjiReturnCode DjiMopChannel_Create(T_DjiMopChannelHandle *channelHandle, E_DjiMopChannelTransType transType);
```

## 通道连接

基于 PSDK 开发的负载设备作为服务器端，在与对端建立连接时，需指定通道的 ID，供客户端绑定。为方便同时与多个客户端建立连接，PSDK 提供了 outChannelHandle 句柄。

1. 通道绑定
   基于 PSDK 开发的负载设备通过指定的 ID 与客户端通信。

```c
T_DjiReturnCode DjiMopChannel_Bind(T_DjiMopChannelHandle channelHandle,
                                   uint16_t channelId);
```

2. 接受连接
   基于 PSDK 开发的负载设备通过如下接口，接受对端发送的连接请求。

```c
T_DjiReturnCode DjiMopChannel_Accept(T_DjiMopChannelHandle channelHandle,
                                     T_DjiMopChannelHandle *outChannelHandle);
```

> **说明：** 该接口为阻塞式的接口，当基于 PSDK 的负载设备作为服务器端时，为能够同时与多个客户端建立连接，请在单独的线程中调用该接口。

## 数据接收

创建通道后，开发者可在该通道上接收对端传输的数据。

```c
T_DjiReturnCode DjiMopChannel_RecvData(T_DjiMopChannelHandle channelHandle,
                                       uint8_t *data,
                                       uint32_t len,
                                       uint32_t *realLen);
```

## 数据发送

创建通道后，开发者可在该通道上向对端发送数据。

```c
T_DjiReturnCode DjiMopChannel_SendData(T_DjiMopChannelHandle channelHandle,
                                       uint8_t *data,
                                       uint32_t len,
                                       uint32_t *realLen);
```

## 关闭通道

通信结束后，请使用如下接口断开与指定通道的连接，释放通道占用的系统资源。

* 关闭通道
  调用如下接口关闭已创建的通道，关闭后，该通道将无法收发数据，但可使与其他通道重新建立连接。

```c
T_DjiReturnCode DjiMopChannel_Close(T_DjiMopChannelHandle channelHandle);
```

* 销毁通道
  调用如下接口销毁指定的通道。

```c
T_DjiReturnCode DjiMopChannel_Destroy(T_DjiMopChannelHandle channelHandle);
```

# 二 功能实现

> 说明
>
> 1. 帧头: 12字节，固定
> 2. len: 4字节，描述帧体长度
> 3. body: 分为状态/图像
> 4. crc: 4字节，固定

## 发送状态

🚀 创建帧体结构体，然后将结构体拷贝到buffer

💡 代码示例如下

```cpp
void MopChannel::createAckBuffer(FrameBody& body)
{
    size_t bodyLength = sizeof(FrameBody);  // 通过结构体计算帧体的大小
    // USER_LOG_INFO("帧体大小: %d", bodyLength);

    memset(sendAckBuffer, 0, SEND_ACK_BUFFER);

    //填充帧头
    const char id[12] = { '4', '5', '9', '4', '5', '4', '1', '4', 'E', '4', '3', '4' };
    memcpy(sendAckBuffer, id, 12);
    int32_t len = bodyLength;
    memcpy(sendAckBuffer + 12, &len, sizeof(len));

    //填充帧体
    memcpy(sendAckBuffer + 16, &body, sizeof(body));

    //填充帧尾
    const char crc[4] = { '4', '7', '5', 'A' };  // 4字节
    memcpy(sendAckBuffer + 16 + sizeof(body), crc, 4);

    ackLength = 12 + 4 + bodyLength + 4;

    SendData(sendAckBuffer, ackLength);
}
```

## 发送图像

🚀 创建帧体结构体，考虑分段， 在每一段赋值后就发送一次

💡 代码示例如下

```cpp
void MopChannel::createImgBuffer(cv::Mat& img, int task_type)
{
    ImgBody body;

    boost::uuids::random_generator generator;
    boost::uuids::uuid             uuid = generator();

    std::string uuid_str = boost::uuids::to_string(uuid);

    body.seg_img_data.clear();

    // 将图像编码为 JPG 格式
    std::vector<uchar> encodedImg;
    std::vector<int>   compression_params = { cv::IMWRITE_JPEG_QUALITY, 90 };
    bool               success            = cv::imencode(".jpg", img, encodedImg, compression_params);

    if (!success)
    {
        std::cerr << "图像编码失败！" << std::endl;
        return;
    }

    body.seg_nums = (encodedImg.size() + SEG_SIZE - 1) / SEG_SIZE;
    std::cout << "\n**************************************************\n"
              << "seg_num: " << body.seg_nums << std::endl;

    // 填充图像分段数据
    for (size_t i = 0; i < body.seg_nums; ++i)
    {
        memset(sendImgBuffer, 0, SEND_IMG_BUFFER);

        //!填充帧头
        const char id[12] = { '4', '5', '9', '4', '5', '4', '1', '4', 'E', '4', '3', '4' };
        memcpy(sendImgBuffer, id, 12);

        // 处理每个分段的图像数据
        int    startIdx = i * SEG_SIZE;
        size_t endIdx   = std::min(static_cast<size_t>(startIdx + SEG_SIZE), encodedImg.size());  // 强制转换为 size_t

        size_t segmentSize = endIdx - startIdx;
        body.seg_img_data.resize(segmentSize);

        //填充长度
        size_t bodyLength = 1 + 1 + 36 + 2 + 2 + segmentSize;

        int32_t len = bodyLength;
        memcpy(sendImgBuffer + 12, &len, sizeof(len));
        // std::cout << "帧体长度：" << len << std::endl;

        //!帧体部分
        body.ack_type           = 1;
        body.fusion_result_type = 1;
        memcpy(sendImgBuffer + 12 + 4, &(body.ack_type), 1);
        memcpy(sendImgBuffer + 12 + 4 + 1, &(body.fusion_result_type), 1);
        memcpy(sendImgBuffer + 12 + 4 + 1 + 1, uuid_str.c_str(), 36);

        body.seg_current_num = i + 1;
        memcpy(sendImgBuffer + 12 + 4 + 1 + 1 + 36, &(body.seg_nums), 2);
        memcpy(sendImgBuffer + 12 + 4 + 1 + 1 + 36 + 2, &(body.seg_current_num), 2);

        //! 图像内容
        memcpy(body.seg_img_data.data(), encodedImg.data() + startIdx, segmentSize);
        memcpy(sendImgBuffer + 12 + 4 + 1 + 1 + 36 + 2 + 2, body.seg_img_data.data(), segmentSize);

        //!填充帧尾
        const char crc[4] = { '4', '7', '5', 'A' };
        memcpy(sendImgBuffer + 12 + 4 + 1 + 1 + 36 + 2 + 2 + segmentSize, crc, 4);

        // 计算最终的 imgLength 并发送数据
        imgLength = 12 + 4 + 1 + 1 + 36 + 2 + 2 + segmentSize + 4;
        SendData(sendImgBuffer, imgLength);
        std::cout << "buffer长度: " << imgLength << std::endl;
    }
}
```
