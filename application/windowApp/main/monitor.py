# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow, QWidget
import paho.mqtt.client as mqtt

from application.windowApp.main.drone import Drone
from application.windowApp.main.mqttRun import MqttRun
from application.windowApp.main.vehicleStatus import VehicleStatus
from application.windowApp.main.vehicleLocation import VehicleLocation

from pyqtlet import L, MapWidget

import gi
from gi.overrides import Gtk

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, GObject, GstVideo

GObject.threads_init()
Gst.init(None)

from application.windowApp.main.mqttClient import MqttClient
from application.windowApp.main.plotCanvas import PlotCanvas

from threadGUI import ThreadGUI
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC


class Monitor(QMainWindow):
    def setupUi(self, MainWindow):
        self.drone = None
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1792, 1008)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_1 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_1.setObjectName("gridLayout_1")

        #self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        #self.verticalLayout_6.setObjectName("verticalLayout_6")


        #self.horizontalLayout = QtWidgets.QHBoxLayout()
        #self.horizontalLayout.setObjectName("horizontalLayout")


        """
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setStretch(1,1)
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        """

        # creat Simple Window
        self.container = QWidget(self)
        self.container.setFixedSize(854,480)
        self.container.setWindowTitle('Test1')

        # container.connect('destroy', self.quit)
        self.setCentralWidget(self.container)
        self.winId = self.container.winId()
        #self.resize(480, 320)

        # Create GStreamer pipeline
        self.videoPipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect('message::error', self.on_error)
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('sync-message::element', self.on_sync_message)
        #self.verticalLayout_8.addWidget(self.container)
        """
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setStretch(1, 1)
        self.verticalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.verticalLayout_10.setObjectName("verticalLayout_10")
        """
        """
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_10.addWidget(self.label_5)
        """
        """
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        """
        # uav detail ui
        self.gridLayout = QtWidgets.QGridLayout()

        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.resize(240, 240)
        self.adi.reinit()
        self.gridLayout.addWidget(self.adi, 0, 0)

        self.alt = qfi_ALT.qfi_ALT(self)
        self.alt.resize(240, 240)

        self.alt.reinit()
        self.gridLayout.addWidget(self.alt, 0, 1)

        self.hsi = qfi_HSI.qfi_HSI(self)
        self.hsi.resize(240, 240)
        self.hsi.reinit()
        self.gridLayout.addWidget(self.hsi, 0, 2)

        self.si = qfi_SI.qfi_SI(self)
        self.si.resize(240, 240)
        self.si.reinit()
        self.gridLayout.addWidget(self.si, 1, 0,1,2,alignment=QtCore.Qt.AlignCenter)

        self.vsi = qfi_VSI.qfi_VSI(self)
        self.vsi.resize(240, 240)
        self.vsi.reinit()
        self.gridLayout.addWidget(self.vsi, 1, 1,1,2,alignment=QtCore.Qt.AlignCenter)

        self.tc = qfi_TC.qfi_TC(self)
        self.tc.resize(240, 240)
        self.tc.reinit()
        #self.gridLayout.addWidget(self.tc, 1, 2)

        self.setLayout(self.gridLayout)
        #self.verticalLayout_10.addLayout(self.gridLayout)


        # end uav detail ui
        #self.gridLayout_1.addLayout(self.verticalLayout_8,0,0)
        self.gridLayout_1.addWidget(self.container,0,0)
        self.gridLayout_1.addLayout(self.gridLayout,0,1)
        #self.horizontalLayout.addLayout(self.verticalLayout_10)
        #self.verticalLayout_6.addLayout(self.horizontalLayout)
        #self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        #self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        #self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        #self.verticalLayout_9.setObjectName("verticalLayout_9")
        """
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        """
        """
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.graphicsView_3.sizePolicy().hasHeightForWidth())
        self.graphicsView_3.setSizePolicy(sizePolicy)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.verticalLayout_9.addWidget(self.graphicsView_3)
        """

        # Map
        self.mapWidget = MapWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.mapWidget.sizePolicy().hasHeightForWidth())
        self.mapWidget.setSizePolicy(sizePolicy)
        self.gridLayout_1.addWidget(self.mapWidget,1,0)
        #self.verticalLayout_9.addWidget(self.mapWidget)
        self.map = L.map(self.mapWidget)

        self.map.setView([22.305711, 114.253426], 20)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)

        self.marker = L.marker([22.305711, 114.253426])
        self.marker.bindPopup('No connection')
        self.map.addLayer(self.marker)

        self.count = 0
        """
        # Working with the maps with pyqtlet

        self.map.setView([22.310409, 114.257598], 20)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)

        #self.marker = L.marker([22.310409, 114.257598])
        #self.marker.bindPopup('UAV Hare')
        #self.map.addLayer(self.marker)
        """

        #self.horizontalLayout_2.addLayout(self.verticalLayout_9)
        #self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        #self.verticalLayout_7.setObjectName("verticalLayout_7")
        """
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        """
        """
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_7.addWidget(self.pushButton)
        """
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        """
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        """
        #self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        #self.scrollArea.setBaseSize(2000,1000)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 849, 1024))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # store graphs

        self.verticalLayout_graphs = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_graphs.setObjectName("verticalLayout_graphs")

        """
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.graphicsView_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_2.setSizePolicy(sizePolicy)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.verticalLayout_7.addWidget(self.graphicsView_2)
        """

        # draw graph
        # 1 PM2.5
        self.data_pm25 = []
        self.data_pm25_time = []
        self.data_pm25_collectTime = []
        self.canvas_pm25 = PlotCanvas(self, width=1, height=4)
        self.canvas_pm25.init_plot("PM2.5", "µg/m³", "Time(s)")
        self.canvas_pm25.setMinimumSize(self.canvas_pm25.size())
        self.verticalLayout_graphs.addWidget(self.canvas_pm25)
        # 2 PM10
        self.data_pm10 = []
        self.data_pm10_time = []
        self.data_pm10_collectTime = []
        self.canvas_pm10 = PlotCanvas(self, width=1, height=4)
        self.canvas_pm10.init_plot("PM10", "µg/m³", "Time(s)")
        self.canvas_pm10.setMinimumSize(self.canvas_pm10.size())
        self.verticalLayout_graphs.addWidget(self.canvas_pm10)
        # 3 temperature
        self.data_temp = []
        self.data_temp_time = []
        self.data_temp_collectTime = []
        self.canvas_temp = PlotCanvas(self, width=1, height=4)
        self.canvas_temp.init_plot("Temperature", "Temperature(C)", "Time(s)")
        self.canvas_temp.setMinimumSize(self.canvas_temp.size())
        self.verticalLayout_graphs.addWidget((self.canvas_temp))
        # 4 humidity
        self.data_hum = []
        self.data_hum_time = []
        self.data_hum_collectTime = []
        self.canvas_hum = PlotCanvas(self, width=1, height=4)
        self.canvas_hum.init_plot("Humidity", "Humidity(%)", "Time(s)")
        self.canvas_hum.setMinimumSize(self.canvas_hum.size())
        self.verticalLayout_graphs.addWidget((self.canvas_hum))

        """
        self.figure_temp = plt.figure(figsize=(1, 2.5))
        self.axes = self.figure_temp.add_subplot(111)
#        FigureCanvas.__init__(self,self.figure_temp)
        FigureCanvas.updateGeometry(self)
#        self.init_plot()
        self.canvas_temp = FigureCanvas(self.figure_temp)
        self.canvas_temp.setMinimumSize(self.canvas_temp.size())
        # fig = plt.gcf()
        # fig.set_size_inches(5, 5)
        # self.toolbar = NavigationToolbar(self.canvas, self)
        plt.suptitle("Temperature")

        # test temperature
        data = [random.random() for i in range(10)]
        self.figure.clear()
        plt.suptitle("Temperature (C)")
        y = (25.2, 25.3, 25.4, 25.7, 25.6, 25.3, 25.4, 25.6, 25.6, 25.7)
        x = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50)
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()

        # self.button = QPushButton('Plot')
        # self.button.clicked.connect(self.plot)
        # layout = QVBoxLayout()
        # self.verticalLayout_7.addWidget(self.toolbar)
        # self.verticalLayout_7.addWidget(self.canvas)
        self.verticalLayout_graphs.addWidget(self.canvas_temp)
        """
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        #self.verticalLayout_7.addWidget(self.scrollArea)
        self.gridLayout_1.addWidget(self.scrollArea,1,1)

        #self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        #self.verticalLayout_6.addLayout(self.horizontalLayout_2)


        # Menu
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1792, 22))
        self.menubar.setObjectName("menubar")
        self.menuMission = QtWidgets.QMenu(self.menubar)
        self.menuMission.setObjectName("menuFile")
        self.menuConnection = QtWidgets.QMenu(self.menubar)
        self.menuConnection.setObjectName("menuConnection")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # new mission
        self.actionNew_Mission = QtWidgets.QAction(MainWindow)
        self.actionNew_Mission.setObjectName("actionNew_Mission")
        self.actionNew_Mission.triggered.connect(self.newMission)
        self.actionView_Mission = QtWidgets.QAction(MainWindow)
        self.actionView_Mission.setObjectName("actionView_Mission")
        # save as
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.saveAs)
        # quit
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.triggered.connect(QApplication.quit)
        # connect
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")

        self.actionConnect.triggered.connect(self.connect)

        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionDisconnect.triggered.connect(self.disconnect)
        self.menuMission.addAction(self.actionNew_Mission)
        self.menuMission.addAction(self.actionSave)
        self.menuMission.addAction(self.actionClose)
        self.menuConnection.addAction(self.actionConnect)
        self.menuConnection.addAction(self.actionDisconnect)
        self.menubar.addAction(self.menuMission.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        # menu button setting
        self.actionConnect.setDisabled(False)
        self.actionDisconnect.setDisabled(True)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.menubar.setNativeMenuBar(False)  # False for current window, True for parent window

        # update detail
        self.updateQFI_thread = VehicleStatus()
        self.updateQFI_thread.updateQFI.connect(self.updateQFI)
        self.updateMap_thread = VehicleLocation()
        self.updateMap_thread.updateMap.connect(self.updateMap)


        self.thread1 = QThread()
        self.thread2 = QThread()
        self.updateQFI_thread.moveToThread(self.thread1)
        self.updateMap_thread.moveToThread(self.thread2)


        MainWindow.setCentralWidget(self.centralwidget)
        """
        #data collect
        from application.windowApp.main.test import MqttClient
        self.client = MqttClient(self)
        self.client.messageSignal.connect(self.on_dataCollected)
        self.client.hostname="navio.local"
        self.client.connectToHost()

        def on_dataCollected(self,msg):
        print("hi")
        """

        # start thread

        self.thread1.started.connect(self.updateQFI_thread.run)
        self.thread1.start()
        self.thread2.started.connect(self.updateMap_thread.run)
        self.thread2.start()

        """
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        """




        #client.loop_forever()
        #if self.drone is not None:

    @QtCore.pyqtSlot(int)
    def on_stateChanged(self, state):
        if state == MqttClient.Connected:
            print(state)
            self.client.subscribe([("/IoTSensor/DHT22",0),("/IoTSensor/SDS011",1)])

    @QtCore.pyqtSlot(str)
    def on_messageSignal(self, msg):
        val = msg
        print(val)
        type = val.split(" ")[1].split("=")[0]
        if type == "Temperature":
            val = val.replace("Time=", "")
            val = val.replace("Temperature=", "")
            val = val.replace("Humidity=", "")
            val = val.split(" ")
            sTime = val[0] #String format
            dTime = datetime.strptime(sTime, '%H:%M:%S') #Time format
            temp = val[1].replace("C", "")
            hum = val[2].replace("%", "")
            self.storeData(self.data_temp,temp,self.data_temp_time,self.data_temp_collectTime,sTime,dTime)
            self.storeData(self.data_hum,hum, self.data_hum_time, self.data_hum_collectTime, sTime, dTime)
        elif type == "PM25":
            val = val.replace("Time=", "")
            val = val.replace("PM25=", "")
            val = val.replace("PM10=", "")
            val = val.split(" ")
            #print(val[0])
            #print(val[1])
            #print(val[2])
            sTime = val[0] #String format
            dTime = datetime.strptime(sTime, '%H:%M:%S') #Time format
            pm25 = val[1]
            pm10 = val[2]
            self.storeData(self.data_pm25,pm25,self.data_pm25_time,self.data_pm25_collectTime,sTime,dTime)
            self.storeData(self.data_pm10,pm10,self.data_pm10_time,self.data_pm10_collectTime,sTime,dTime)
        self.draw()


    def storeData(self, target, data,target_time,target_collectTime, sTime,dTime):
        print(data)
        target.append(float(data))

        if (len(target_time) != 0):
            lTime = datetime.strptime(target_collectTime[-1], '%H:%M:%S') #lastest collect time
            timeDiff = dTime-lTime
            #print(target_collectTime[-1],sTime)
            #print(timeDiff.seconds)
            target_time.append(target_time[-1] + int(str(timeDiff.seconds)))
            target_collectTime.append(sTime)
        else:
            print('first')
            target_time.append(0)
            target_collectTime.append(sTime)

    def draw(self):
        # print("draw")
        self.canvas_pm25.update_figure(self.data_pm25_time,self.data_pm25)
        self.canvas_pm10.update_figure(self.data_pm10_time, self.data_pm10)
        self.canvas_temp.update_figure(self.data_temp_time, self.data_temp)
        self.canvas_hum.update_figure(self.data_hum_time, self.data_hum)

    """"@QtCore.pyqtSlot(str)
    def on_message(self,client,userdata,msg):
        try:
            print(msg)
            val = msg
            for s in val:
                print(s)
            type = val.split(" ")[1].split("=")[0]
            if(type == "Temperature"):
                val = val.replace("Time=", "")
                val = val.replace("Temperature=", "")
                val = val.replace("Humidity=", "")
                val = val.split(" ")
                print(val[0])
                print(val[1])
                print(val[2])
                self.storeData(self.data_temp, val[1].replace("C", ""), val[0])
                self.storeData(self.data_hum, val[2].replace("%", ""), val[0])"""
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
        #except ValueError:
            #print("error: Not is number")



    def saveAs(self):
        # file_path = mdd.makeDirectory()
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        directory = time.strftime('%d-%m-%Y') + ' ' + time.strftime('%H-%M-%S')

        # print(path)
        if path != "":
            path = path + "/" + directory
            os.mkdir(path)
            record = open(path + "/" + 'raw_data.txt', 'a+')
            output_temp = ""
            output_hum = ""
            try:
                if len(self.data_temp) != 0:
                    output_temp = ["%.1f" % number for number in self.data_temp]
                    output_temp = ','.join(output_temp)
                if len(self.data_hum != 0):
                    output_hum = ["%.1f" % number for number in self.data_hum]
                    output_hum = ','.join(output_hum)
            except:
                pass
            # print(output_temp)

            output = "{\n" \
                     "\"Temperature\":{" \
                     "\n\t\"Data\":[" + output_temp + "],\n\t\"Unit\":5," \
                                                      "\n\t\"Humidity\":[" + output_hum + "],\n\t\"Unit\":5\n\t}\n}"
            record.write(output)
            self.canvas_temp.outputImage(path + "/" + "Temperature")
            self.canvas_hum.outputImage(path + "/" + "Humidity")

    def newMission(self):
        msgBox = QMessageBox()
        msgBox.setText("Do you want to create a new mission now? If yes, then the current mission will be closed.")
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        option = msgBox.exec_()
        if option == QMessageBox.Ok:
            # os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
            os.execl(sys.executable, sys.executable, *sys.argv)
            # os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)

    def videoPipeline(self):
        self.pipeline = Gst.Pipeline()
        self.tcpsrc = Gst.ElementFactory.make('tcpclientsrc', 'tcpsrc')
        self.tcpsrc.set_property("host", '192.168.12.1')
        self.tcpsrc.set_property("port", 5000)

        self.gdepay = Gst.ElementFactory.make('gdpdepay', 'gdepay')

        self.rdepay = Gst.ElementFactory.make('rtph264depay', 'rdepay')

        self.avdec = Gst.ElementFactory.make('avdec_h264', 'avdec')

        self.vidconvert = Gst.ElementFactory.make('videoconvert', 'vidconvert')

        self.asink = Gst.ElementFactory.make('autovideosink', 'asink')
        self.asink.set_property('sync', False)
        # self.asink.set_property('emit-signals', True)
        # self.set_property('drop', True)

        self.pipeline.add(self.tcpsrc)
        self.pipeline.add(self.gdepay)

        self.pipeline.add(self.avdec)

        self.pipeline.add(self.rdepay)

        self.pipeline.add(self.vidconvert)
        self.pipeline.add(self.asink)

        self.tcpsrc.link(self.gdepay)
        self.gdepay.link(self.rdepay)
        self.rdepay.link(self.avdec)
        self.avdec.link(self.vidconvert)
        self.vidconvert.link(self.asink)

    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            message.src.set_property('force-aspect-ratio', True)
            message.src.set_window_handle(self.winId)

    def quit(self, container):
        self.pipeline.set_state(Gst.State.NULL)
        # self.pipeline_A.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        # self.pipeline_A.set_state(Gst.State.PLAYING)
        # self.showMaximized()
        # self.verticalLayout_8.addWidget(self)

    def updateQFI(self, detail):
        if(detail["airspeed"] != ""):
            self.adi.setRoll(math.degrees(detail["attitude_roll"]))
            self.adi.setPitch(math.degrees(detail["attitude_pitch"]))
            self.alt.setAltitude(detail["altitude"])
            self.si.setSpeed(detail["airspeed"])
            self.hsi.setHeading(detail["heading"])
            self.vsi.setClimbRate(detail["verticalSpeed"])

            self.adi.viewUpdate.emit()
            self.alt.viewUpdate.emit()
            self.si.viewUpdate.emit()
            self.hsi.viewUpdate.emit()
            self.vsi.viewUpdate.emit()
            #print('QFI')

    def updateMap(self, detail):

        # Working with the maps with pyqtlet
        if (detail["location_lat"] != ""):
            # print(str(detail["location_lat"])+","+str(detail["location_lon"]))
            self.map.removeLayer(self.marker)
            if self.count == 0:
                self.map.setView([detail["location_lat"], detail["location_lon"]], 20)
            self.count += 1
            if self.count % 10 == 0:
                self.map.setView([detail["location_lat"], detail["location_lon"]], 20)
            self.marker = L.marker([detail["location_lat"], detail["location_lon"]])
            self.marker.bindPopup('UAV Here')
            self.map.addLayer(self.marker)
            #print("Map")



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Automated Data Collecting System"))
        #self.label.setText(_translate("MainWindow", "Streaming"))
        #self.label_5.setText(_translate("MainWindow", "UAV Details"))
        # self.label_7.setText(_translate("MainWindow", "Airspeed"))
        # self.label_6.setText(_translate("MainWindow", "Groundspeed"))
        # self.label_4.setText(_translate("MainWindow", "Attitude"))
        # self.label_3.setText(_translate("MainWindow", "Heading"))
        # self.label_8.setText(_translate("MainWindow", "Altitude"))
        # self.label_10.setText(_translate("MainWindow", "Vertical Speed"))
        #self.label_9.setText(_translate("MainWindow", "Map"))
        #self.label_2.setText(_translate("MainWindow", "Data Collection"))
        #self.pushButton.setText(_translate("MainWindow", "Start"))
        self.menuMission.setTitle(_translate("MainWindow", "Mission"))
        self.menuConnection.setTitle(_translate("MainWindow", "Connection"))
        self.actionNew_Mission.setText(_translate("MainWindow", "New Mission"))
        self.actionView_Mission.setText(_translate("MainWindow", "View Mission"))
        self.actionSave.setText(_translate("MainWindow", "Save As"))
        self.actionClose.setText(_translate("MainWindow", "Quit"))
        self.actionConnect.setText(_translate("MainWindow", "Connect"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))

    """
        def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        plt.suptitle("Temperature (C)")
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()
    """

    def connect(self):
        # self.drone = Drone('tcp:127.0.0.1:5760')
        self.drone = Drone('udp:0.0.0.0:14550')
        #print("connect")
        #print(self.drone.isconnect)
        if self.drone.isconnect == True:
            self.vehicle = self.drone.getDrone()
            self.actionConnect.setDisabled(True)
            self.actionDisconnect.setDisabled(False)

            #MQtt start
            self.client = MqttClient(self)
            self.client.stateChanged.connect(self.on_stateChanged)
            self.client.messageSignal.connect(self.on_messageSignal)
            self.client.hostname = "192.168.12.1"
            self.client.connectToHost()

            #start Map and QFI
            self.updateMap_thread.setVehicle(self.vehicle)
            self.updateQFI_thread.setVehicle(self.vehicle)
            self.start()

            # Animation thread
            t2 = ThreadGUI(self.gridLayout)
            t2.daemon = True
            t2.start()
        else:
            self.disconnect()


    def disconnect(self):
        self.drone.disconnectDrone()
        self.actionConnect.setDisabled(False)
        self.actionDisconnect.setDisabled(True)
        self.updateMap_thread.exist = False
        self.updateQFI_thread.exist = False
        self.quit(self.container)

        self.adi.setRoll(0)
        self.adi.setPitch(0)
        self.alt.setAltitude(0)
        self.si.setSpeed(0)
        self.hsi.setHeading(0)
        self.vsi.setClimbRate(0)

        self.adi.viewUpdate.emit()
        self.alt.viewUpdate.emit()
        self.si.viewUpdate.emit()
        self.hsi.viewUpdate.emit()
        self.vsi.viewUpdate.emit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Monitor()
    ui.setupUi(MainWindow)
    # ui.start()
    MainWindow.show()
    sys.exit(app.exec_())
