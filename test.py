import time

import paho.mqtt.client as mqtt


def on_connect(mosq, obj, flags, rc):
    print ('on_connect:: Connected with result code ' + str(rc))
    print('rc: ' + str(rc))


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_log(mosq, obj, level, string):
    print(string)

client = mqtt.Client()
# Assign event callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Uncomment to enable debug messages
client.on_log = on_log

# Connect to the Broker
client.connect('192.168.12.1', 1883, 60)
client.subscribe([('/IoTSensor/DHT22', 0), ('/IotSensor/SDS011', 0)])
time.sleep(1)

client.loop_forever()


