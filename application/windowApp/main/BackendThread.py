
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
                detail = {"airSpeed": self.vehicle.airspeed, "attltude": self.vehicle.attitude, "altitude": "",
                          "turnCoordinator": "", "heading": self.vehicle.heading, "verticalSpeed": ""}
            else:
                detail = {"airSpeed": "", "attltude": "", "altitude": "",
                          "turnCoordinator": "", "heading": "", "verticalSpeed": ""}
            #self.update_detail.emit(detail["airSpeed"],detail["attltude"],detail["altitude"],detail["turnCoordinator"],detail["heading"],detail["verticalSpeed"])
            self.update_detail.emit(detail)
            time.sleep(1)
    def setVehicle(self,vehicle):
        self.vehicle=vehicle
        self.exist=True
