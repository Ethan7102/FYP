import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ExampleWindow(QMainWindow):
    def __init__(self, windowsize):
        super().__init__()
        self.windowsize = windowsize
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)

        widget = QWidget()
        self.setCentralWidget(widget)
        pixmap1 = QPixmap(os.path.join('airspeed_markings.svg'))
        pixmap1 = pixmap1.scaledToWidth(self.width())
        self.image = QLabel()
        self.image.setPixmap(pixmap1)

        layout_box = QHBoxLayout(widget)
        layout_box.setContentsMargins(0, 0, 0, 0)
        layout_box.addWidget(self.image)

        pixmap2 = QPixmap(os.path.join('airspeed_hand.svg'))
        self.image2 = QLabel(widget)
        self.image2.setPixmap(pixmap2)
        self.image2.setFixedSize(pixmap2.size())

        p = self.geometry().bottomRight() - self.image2.geometry().bottomRight()
        self.image2.move(p)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.rotate(150)
        painter.drawPixmap()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screensize = app.desktop().availableGeometry().size()

    ex = ExampleWindow(screensize)
    ex.show()

    sys.exit(app.exec_())
