---
layout:     post

title:      PSDK 拉取DJI M3T 流

date:       2024-12-02

author:     phoenixZ

header-img: img/dji2.jpg

catalog: true

tags:

    - dji

    - psdk
---
> 说明: 测试环境为：
>
> * PSDK: 3.9.2
> * 飞行器: M3T
> * 解码器: FFMPEG(软解码)

# 拉流流程

1. 初始化拉流模块

   ```cpp
       returnCode = DjiLiveview_Init();
   ```
2. 开始拉流

   ```cpp
       DjiLiveview_StartH264Stream(DJI_LIVEVIEW_CAMERA_POSITION_NO_1, DJI_LIVEVIEW_CAMERA_SOURCE_M3T_IR, &StreamDecoder::startIrCameraDecoding);
       DjiLiveview_StartH264Stream(DJI_LIVEVIEW_CAMERA_POSITION_NO_1, DJI_LIVEVIEW_CAMERA_SOURCE_DEFAULT, &StreamDecoder::startMainCameraDecoding);

   ```
   API解释：

   - position ：指定输出h264流的摄像头位置
   - source： 指定摄像头
   - callback: 当接收到新的H264帧时，会在接收到新帧的时候调用

   ```cpp
   void StreamDecoder::startMainCameraDecoding(E_DjiLiveViewCameraPosition position, const uint8_t* buf, uint32_t bufLen)
   {
       if (!mainCameraDecoderState.isInitialized)
       {
           initDecoder(mainCameraDecoderState);
       }

       cv::Mat frame;
       decodeStream(buf, bufLen, mainCameraDecoderState, frame);

       if (!frame.empty())
       {
           std::lock_guard<std::mutex> lock(frameMutex);
           mainFrameQueue.push(frame);
       }
   }
   ```
3. 解码， 使用FFMPEG

   - 初始化解码参数
   - 利用解码器将buf转换成cv::Mat

   ⭐️ 解码部分移步至解码blog
4. 停止拉流

   ```cpp
   T_DjiReturnCode DjiLiveview_StopH264Stream(E_DjiLiveViewCameraPosition position, E_DjiLiveViewCameraSource source);
   ```
