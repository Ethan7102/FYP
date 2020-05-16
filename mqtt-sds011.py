#!/usr/bin/python
from __future__ import print_function
import serial
import struct
import os
import sys
import time
import subprocess
import paho.mqtt.client as mqtt

DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1
PERIOD_CONTINUOUS = 0

SDS011 = serial.Serial()
SDS011.port = "/dev/ttyUSB0"
SDS011.baudrate = 9600

SDS011.open()
SDS011.flushInput()

byte, data = 0, ""


def dump(d, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in d))


def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0, ] * (12 - len(data))
    checksum = (sum(data) + cmd - 2) % 256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret


def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]


def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8]) % 256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]),
                                                       "OK" if (checksum == r[4] and r[5] == 0xab) else "NOK"))


def read_response():
    byte = 0
    while byte != "\xaa":
        byte = SDS011.read(size=1)

    d = SDS011.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d


def cmd_set_mode(mode=MODE_QUERY):
    SDS011.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()


def cmd_query_data():
    SDS011.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values


def cmd_set_sleep(sleep):
    mode = 0 if sleep else 1
    SDS011.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()


def cmd_set_working_period(period):
    SDS011.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()


def cmd_firmware_ver():
    SDS011.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)


def cmd_set_id(id):
    id_h = (id >> 8) % 256
    id_l = id % 256
    SDS011.write(construct_command(CMD_DEVICE_ID, [0] * 10 + [id_l, id_h]))
    read_response()


# Define event callbacks
def on_connect(mosq, obj, flags, rc):
    print ('on_connect:: Connected with result code ' + str(rc))
    print('rc: ' + str(rc))


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_log(mosq, obj, level, string):
    print(string)


if __name__ == "__main__":
    client = mqtt.Client()
    # Assign event callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Uncomment to enable debug messages
    client.on_log = on_log

    # Connect to the Broker
    client.connect('localhost', 1883, 60)
    time.sleep(1)

    client.loop_start()

    run = True

    try:
        record = open('/home/pi/pm25.csv', 'a+')
        if os.stat('/home/pi/pm25.csv').st_size == 0:
            record.write('Date,Time,PM2.5,PM10\r\n')
    except:
        pass

    cmd_set_sleep(0)
    cmd_firmware_ver()
    cmd_set_working_period(PERIOD_CONTINUOUS)
    cmd_set_mode(MODE_QUERY);

    try:
        while True:
            cmd_set_sleep(0)
            for t in range(15):
                values = cmd_query_data();
                if values is not None and len(values) == 2:
                    print("PM2.5: ", values[0], ", PM10: ", values[1])
                    record.write('{0}, {1}, {2:0.1f}C, {3:0.1f}%\r\n'.format(time.strftime('%d/%m/%Y'),
                                                                             time.strftime('%H:%M:%S'),  values[0],
                                                                             values[1]))
                    # Send messages to the Broker
                    client.publish("/IoTSensor/DHT22",
                                   "Temperature={0:0.1f}C  Humidity={1:0.1f}%".format(values[0], values[1]))
                    time.sleep(2)

            print("Going to sleep for 1 min...")
            cmd_set_sleep(1)
            time.sleep(60)

    except KeyboardInterrupt:
        print('exiting')
        client.disconnect()
        client.loop_stop()