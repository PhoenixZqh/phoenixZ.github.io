---
layout:     post

title:      PSDK 订阅飞机信息

date:       2024-12-02

author:     phoenixZ

header-img: img/dji3.jpg

catalog: true

tags:

    - dji

    - psdk
---
# 一 流程

1. 初始化订阅模块

   ```cpp
   DjiFcSubscription_Init();
   ```
2. 在线程函数中订阅无人机上的信息

   ```cpp
   DjiFcSubscription_SubscribeTopic(DJI_FC_SUBSCRIPTION_TOPIC_POSITION_VO, DJI_DATA_SUBSCRIPTION_TOPIC_50_HZ, positionCB);
       if (djistat_ != DJI_ERROR_SYSTEM_MODULE_CODE_SUCCESS)
   ```
3. 回调函数解析数据

   ```cpp
   T_DjiReturnCode DroneSubscription::positionCB(const uint8_t* data, uint16_t dataSize, const T_DjiDataTimestamp* timestamp)
   {
       T_DjiFcSubscriptionPositionVO* pos = (T_DjiFcSubscriptionPositionVO*)data;
       dji_.position_vo                   = std::make_pair(*timestamp, *pos);
       return DJI_ERROR_SYSTEM_MODULE_CODE_SUCCESS;
   }
   ```

# 二 注意事项

1. 需注意订阅项支持的订阅频率
2. 每个订阅项支持重复订阅

<div>
<div div style="text-align: center"><p>表. 飞行器订阅项</p></div>
<div>
<table width="100%" style=" hyphens: auto; display: table; table-layout:fixed;">
    <thead>
        <tr>
            <th width="40%">数据订阅 TOPIC</th>
            <th>M300 RTK</th>
            <th>Matrice 30/30T</th>
            <th>Mavic 3E/3T</th>
            <th>Matrice 3D/3TD</th>
            <th>Flycart 30</th>
            <th>M350 RTK</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>姿态四元数<br/>*_QUATERNION</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>相对地面加速度<br/>*_ACCELERATION_GROUND</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>相对机体加速度<br/>*_ACCELERATION_BODY</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>原始加速度<br/>*_ACCELERATION_RAW</td>
            <td>最大 400Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 400Hz</td>
        </tr>
        <tr>
            <td>速度<br/>*_VELOCITY</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>融合角速度<br/>*_ANGULAR_RATE_FUSIONED</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>原始角速度<br/>*_ANGULAR_RATE_RAW</td>
            <td>最大 400Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 400Hz</td>
        </tr>
        <tr>
            <td>融合高度<br/>*_ALTITUDE_FUSED</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>气压计高度<br/>*_ALTITUDE_BAROMETER</td>
            <td>最大 200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>Home 点高度<br/>*_ALTITUDE_OF_HOMEPOINT</td>
            <td>最大 1Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 1Hz</td>
        </tr>
        <tr>
            <td>融合相对地面高度<br/>*_HEIGHT_FUSION</td>
            <td>最大 100Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 100Hz</td>
        </tr>
        <tr>
            <td>相对地面高度<br/>*_HEIGHT_RELATIVE</td>
            <td>最大 200Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>融合位置坐标<br/>*_POSITION_FUSED</td>
            <td>最大 200Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 200Hz</td>
        </tr>
        <tr>
            <td>GPS 日期（年月日）<br/>*_GPS_DATE</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>GPS 时间（时分秒）<br/>*_GPS_TIME</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>GPS 位置<br/>*_GPS_POSITION</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>GPS 速度<br/>*_GPS_VELOCITY</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>GPS 信息<br/>*_GPS_DETAILS</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>GPS 信号强度<br/>*_GPS_SIGNAL_LEVEL</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>RTK 位置<br/>*_RTK_POSITION</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>RTK 速度<br/>*_RTK_VELOCITY</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>RTK 航向角<br/>*_RTK_YAW</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>RTK 位置信息<br/>*_RTK_POSITION_INFO</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>RTK 航向信息<br/>*_RTK_YAW_INFO</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
        </tr>
        <tr>
            <td>指南针信息<br/>*_COMPASS</td>
            <td>最大 100Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 100Hz</td>
        </tr>
        <tr>
            <td>遥控摇杆信息<br/>*_RC</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>云台角度<br/>*_GIMBAL_ANGLES</td>
            <td>最大 50Hz</td>
            <td>仅支持 50Hz</td>
            <td>仅支持 50Hz</td>
            <td>仅支持 50Hz</td>
            <td>仅支持 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>云台状态<br/>*_GIMBAL_STATUS</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>飞行状态<br/>*_STATUS_FLIGHT</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>飞行模式状态<br/>*_STATUS_DISPLAYMODE</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>起落架状态<br/>*_STATUS_LANDINGGEAR</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>电机启动错误码<br/>*_STATUS_MOTOR_START_ERROR</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>电池信息<br/>*_BATTERY_INFO</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>设备控制信息<br/>*_CONTROL_DEVICE</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>硬件时钟同步<br/>*_HARD_SYNC</td>
            <td>400Hz</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>400Hz</td>
        </tr>
        <tr>
            <td>GPS 控制等级<br/>*_GPS_CONTROL_LEVEL</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>带标记遥控遥感信息<br/>*_RC_WITH_FLAG_DATA</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>电调数据<br/>*_ESC_DATA</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>RTK 连接状态<br/>*_RTK_CONNECT_STATUS</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>云台控制模式<br/>*_GIMBAL_CONTROL_MODE</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>飞行异常信息<br/>*_FLIGHT_ANOMALY</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>笛卡尔坐标位置<br/>*_POSITION_VO</td>
            <td>200Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>200Hz</td>
        </tr>
        <tr>
            <td>避障数据<br/>*_AVOID_DATA</td>
            <td>最大 100Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 100Hz</td>
        </tr>
        <tr>
            <td>返航点设置状态<br/>*_HOME_POINT_SET_STATUS</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>返航点信息<br/>*_HOME_POINT_INFO</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 5Hz</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>三云台信息<br/>（适用M300 RTK与M350 RTK，上下三个云台的信息）<br/>*_THREE_GIMBAL_DATA</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>1 号电池信息<br/>*_BATTERY_SINGLE_INFO_INDEX1</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
        <tr>
            <td>2 号电池信息<br/>*_BATTERY_SINGLE_INFO_INDEX2</td>
            <td>最大 50Hz</td>
            <td>最大 50Hz</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>最大 50Hz</td>
        </tr>
    </tbody>
</table></div></div>
