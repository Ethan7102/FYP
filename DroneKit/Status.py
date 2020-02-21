# -*- coding: utf-8 -*-
# Import DroneKit-Python
from dronekit import connect, Command, LocationGlobal, VehicleMode
from pymavlink import mavutil
import time, sys, argparse, math

# Connect to the Vehicle
print("Connecting")
connection_string = '0.0.0.0:14550'
vehicle = connect(connection_string, wait_ready=True)

# Display basic vehicle state
# 飞控软件版本
print("Autopilot Firmware version: %s" % vehicle.version)
# 全球定位信息（经纬度，高度相对于平均海平面）
print("Global Location: %s" % vehicle.location.global_frame)
# 全球定位信息（经纬度，高度相对于home点）
print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
# 相对home点的位置信息（向北、向东、向下）；解锁之前返回None
print("Local Location: %s" % vehicle.location.local_frame)
# 无人机朝向（欧拉角：roll，pitch，yaw，单位为rad，范围-π到+π）
print("Attitude: %s" % vehicle.attitude)
# 三维速度（m/s）
print("Velocity: %s" % vehicle.velocity)
# GPS信息
print("GPS: %s" % vehicle.gps_0)
# 地速（m/s）
print("Groundspeed: %s" % vehicle.groundspeed)
# 空速（m/s）
print("Airspeed: %s" % vehicle.airspeed)
# 云台信息（得到的为当前目标的roll, pitch, yaw，而非测量值。单位为度）
print("Gimbal status: %s" % vehicle.gimbal)
# 电池信息
print("Battery: %s" % vehicle.battery)
# EKF（拓展卡曼滤波器）状态
print("EKF OK?: %s" % vehicle.ekf_ok)
# 超声波或激光雷达传感器状态
print("Rangefinder: %s" % vehicle.rangefinder)
# 无人机朝向（度）
print("Heading: %s" % vehicle.heading)
# 是否可以解锁
print("Is Armable?: %s" % vehicle.is_armable)
# 系统状态
print("System status: %s" % vehicle.system_status.state)
# 当前飞行模式
print("Mode: %s" % vehicle.mode.name)
# 解锁状态
print("Armed: %s" % vehicle.armed)

print("\nPrint all parameters (iterate `vehicle.parameters`):")
for key, value in vehicle.parameters.items():
    print(" Key:%s Value:%s" % (key, value))
