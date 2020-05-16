from PyQt5.QtCore import QObject
import paho.mqtt.client as mqtt


class MqttRun(QObject):
    def run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("192.168.12.1", 1883, 60)

        self.client.loop_forever()



    def on_connect(client, userdata, rc):
        # if state == MqttClient.Connected:
        toptics = [("/IoTSensor/DHT22", 1), ("/IoTSensor/SDS011", 1)]
        for toptic in toptics:
            client.subscribe(toptic)

    # else:
    # print("empty")

    def on_message(client, userdata, msg):
        try:
            print(msg)
            """
            val = msg
            for s in val:
                print(s)
            type = val.split(" ")[1].split("=")[0]
            if (type == "Temperature"):
                val = val.replace("Time=", "")
                val = val.replace("Temperature=", "")
                val = val.replace("Humidity=", "")
                val = val.split(" ")
                print(val[0])
                print(val[1])
                print(val[2])
                self.storeData(self.data_temp, val[1].replace("C", ""), val[0])
                self.storeData(self.data_hum, val[2].replace("%", ""), val[0])
                
            """
            """
            val = val.replace("Temperature=", "")
            val = val.replace("Humidity=", "")
            val = val.split(" ")
            print(msg)
            self.storeData(self.data_temp, val[0].replace("C", ""), self.data_temp_time)
            self.storeData(self.data_hum, val[2].replace("%", ""), self.data_hum_time)
            """
            # self.label_5.setText(val)
            """
            for x in self.data_temp:
                print(x)
            for x in self.data_temp_time:
                print(x)
            """
            #self.draw()
        except ValueError:
            print("error: Not is number")