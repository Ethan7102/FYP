
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
                detail = {"airspeed": self.vehicle.airspeed, "attltude": self.vehicle.attitude, "altitude": self.vehicle.location.global_relative_frame.alt,
                          "groundspeed": self.vehicle.groundspeed, "heading": self.vehicle.heading, "verticalSpeed": self.vehicle.velocity}
            else:
                detail = {"airspeed": "", "attltude": "", "altitude": "",
                          "groundspeed": "", "heading": "", "verticalSpeed": ""}
            self.update_detail.emit(detail)
            time.sleep(1)
    def setVehicle(self,vehicle):
        self.vehicle=vehicle
        self.exist=True
