from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
import time
import sys


class VehicleStatus(QObject):
    update_detail = pyqtSignal(object)
    exist = False

    def run(self):
        while True:
            if (self.exist):
                # split attitude
                attitude = str(self.vehicle.attitude).split(':')
                print(attitude)
                attitude = attitude[1].split('=')
                attitude_pitch =float(attitude[1].split(',')[0])
                attitude_yaw =float(attitude[2].split(',')[0])
                attitude_roll =float(attitude[3].split(',')[0])
                detail = {"airspeed": self.vehicle.airspeed,
                          "attitude_pitch": attitude_pitch,
                          "attitude_yaw": attitude_yaw,
                          "attitude_roll": attitude_roll,
                          "altitude": self.vehicle.location.global_relative_frame.alt,
                          "groundspeed": format(float(self.vehicle.groundspeed), '0.3f'),
                          "heading": self.vehicle.heading,
                          "verticalSpeed": self.vehicle.velocity[2],
                          "location_lat": self.vehicle.location.global_frame.lat,
                          "location_lon": self.vehicle.location.global_frame.lon}
                print(detail["verticalSpeed"])
            else:
                detail = {"airspeed": "", "attitude_pitch": "", "attitude_yaw": "", "attitude_roll": "", "altitude": "",
                          "groundspeed": "", "heading": "", "verticalSpeed": "", "location_lat": "", "location_lon": ""}
            self.update_detail.emit(detail)
            time.sleep(1)

    def setVehicle(self, vehicle):
        self.vehicle = vehicle
        self.exist = True
