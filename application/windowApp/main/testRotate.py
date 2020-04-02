from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject

from PyQt5.QtCore import QTimer, QPoint, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor, QPixmap
import sys

app = QtWidgets.QApplication(sys.argv)

widget = QtWidgets.QLabel()
widget.setGeometry(50,200,500,500)
renderer =  QtSvg.QSvgRenderer('img/attitude_roll_2.svg')
widget.resize(renderer.defaultSize())
painter = QtGui.QPainter(widget)
painter.restore()
renderer.render(painter)
widget.show()

sys.exit(app.exec_())