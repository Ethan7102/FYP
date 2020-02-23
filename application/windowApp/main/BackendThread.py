
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
import time
import sys

class BackendThread(QObject):

    update_detail=pyqtSignal(object)
    exist=False
    def run(self):
        while True:
            if(self.exist):
                #split attitude
                attitude = str(self.vehicle.attitude).split(':')
                attitude = attitude[1].split('=')
                attitude_pitch = "pitch:"+format(float(attitude[1].split(',')[0]),'0.3f')
                attitude_yaw ="yaw:"+format(float(attitude[2].split(',')[0]),'0.3f')
                attitude_roll = "roll:"+format(float(attitude[3].split(',')[0]),'0.3f')

                detail = {"airspeed": self.vehicle.airspeed, "attitude_pitch": attitude_pitch, "attitude_yaw":attitude_yaw,"attitude_roll":attitude_roll,"altitude": self.vehicle.location.global_relative_frame.alt,
                          "groundspeed": self.vehicle.groundspeed, "heading": self.vehicle.heading, "verticalSpeed": self.vehicle.velocity}
            else:
                detail = {"airspeed": "", "attitude_pitch": "","attitude_yaw":"","attitude_roll":"", "altitude": "",
                          "groundspeed": "", "heading": "", "verticalSpeed": ""}
            self.update_detail.emit(detail)
            time.sleep(1)
    def setVehicle(self,vehicle):
        self.vehicle=vehicle
        self.exist=True
