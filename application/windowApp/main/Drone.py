import dronekit_sitl
from dronekit import connect, VehicleMode
class Drone:

    def __init__(self,connection_string):
        self.connection_string=connection_string
        self.sitl = dronekit_sitl.start_default()
        #self.drone = connect(self.connection_string, wait_ready=True)
        self.drone = connect('tcp:127.0.0.1:5760', wait_ready=True)

    def connectDrone(self):
        self.drone = connect(self.connection_string, wait_ready=True)

    def getDrone(self):
        return self.drone
    def disconnectDrone(self):
        self.drone.close()
        self.sitl.stop()
        #print("Completed")