#!/usr/bin/python


import datetime
import signal
import sys
from collections import defaultdict
from subprocess import Popen, PIPE
import subprocess

import re

try:
    import picamera
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "picamera"])
finally:
    import picamera

DNSMASQ_LEASES_FILE = "/var/lib/misc/dnsmasq.leases"


class LeaseEntry:
    def __init__(self, leasetime, macAddress, ipAddress, name):
        if (leasetime == '0'):
            self.staticIP = True
        else:
            self.staticIP = False
        self.leasetime = datetime.datetime.fromtimestamp(
            int(leasetime)
        ).strftime('%Y-%m-%d %H:%M:%S')
        self.macAddress = macAddress.upper()
        self.ipAddress = ipAddress
        self.name = name

    def serialize(self):
        return {
            'staticIP': self.staticIP,
            'leasetime': self.leasetime,
            'macAddress': self.macAddress,
            'ipAddress': self.ipAddress,
            'name': self.name
        }


def leaseSort(arg):
    # Fixed IPs first
    if arg.staticIP == True:
        return '0' + arg.ipAddress
    else:
        return arg.ipAddress


def getLeases():
    leases = list()
    with open(DNSMASQ_LEASES_FILE) as f:
        for line in f:
            elements = line.split()
            if len(elements) == 5:
                entry = LeaseEntry(elements[0],
                                   elements[1],
                                   elements[2],
                                   elements[3])
                leases.append(entry)
    leases.sort(key=leaseSort)
    leases = [lease.serialize() for lease in leases]
    return leases


if __name__ == "__main__":
    while True:
        for item in getLeases():
            print(item['ipAddress'])

            # start the gstreamer process with a pipe for stdin
            gstreamer = subprocess.Popen([
                'gst-launch-1.0', '-v',
                'fdsrc',
                '!', 'h264parse',
                '!', 'rtph264pay', 'config-interval=1', 'pt=96',
                '!', 'udpsink', 'host=' + item['ipAddress'], 'port=5600'
            ], stdin=subprocess.PIPE)

            # initialize the camera
            camera = picamera.PiCamera(resolution=(1280, 720), framerate=30)
            camera.hflip = True

            # start recording to gstreamer's stdin
            camera.start_recording(gstreamer.stdin, format='h264', bitrate=4000000)
