# -*-coding:utf-8-*-

import sys
from datetime import datetime

from PyQt5 import QtSvg
from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtGui import QColor, QPalette, QBrush, QPixmap, QPolygon, QPainter
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtWidgets import QWidget, QApplication, QAction, QLabel
from PyQt5.uic.properties import QtGui, QtCore


class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)

        self.checktime()

        self.hourColor = QColor(127, 0, 127);
        self.minuteColor = QColor(0, 127, 127, 191)
        self.secondColor = QColor(127, 127, 0, 120)
        self.airspeedHandColor = QColor('white');

        self.initUI()

        quitAction = QAction("E&xit", self, shortcut="Ctrl+Q",
                             triggered=QApplication.instance().quit)
        self.addAction(quitAction)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # 毫秒
        self.timer.timeout.connect(self.update)
        self.timer.start()

        self.rightButton = False

        print(self.width())
        print(self.height())

    def handChange(self):
        self.side = min(self.width(), self.height())
        self.hand = (max(self.side / 200, 4), max(self.side / 100, 8), max(self.side / 40, 30))
        self.airspeedHand = QPolygon(
            [QPoint(self.hand[0], self.hand[1]), QPoint(-self.hand[0], self.hand[1]), QPoint(0, -self.hand[2] * 1.6)])
        self.test = QPolygon(
            [QPoint(self.hand[0], self.hand[1]), QPoint(0, -self.hand[2] * -0.5), QPoint(-self.hand[0], self.hand[1]),
             QPoint(0, -self.hand[2] * 1.6)])

    def initUI(self):
        self.setFixedSize(400, 400)
        self.handChange()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.draw(event, qp)
        qp.end()

    def draw(self, event, qp):
        self.checktime()
        qp.translate(self.width() / 2, self.height() / 2)
        qp.scale(self.side / 200.0, self.side / 200.0)

        qp.setPen(Qt.NoPen)
        qp.setBrush(self.airspeedHandColor)
        qp.save()
        qp.rotate(30.0 * ((self.time.hour + self.time.minute / 60.0)))
        qp.drawConvexPolygon(self.test)
        #qp.drawRect(self.test)
        qp.restore()


    def checktime(self):
        self.time = datetime.now()
        self.hour = self.time.hour
        self.minute = self.time.minute
        self.second = self.time.second


def main():
    app = QApplication(sys.argv)
    palette = QPalette()

    brush = QBrush(QColor(0, 0, 0, 0), QPixmap("clock.png"))
    palette.setBrush(QPalette.Window, brush)
    clock = Clock()
    clock.setPalette(palette)
    clock.show()

    """svgWidget = QSvgWidget()
    svgWidget.renderer().load("airspeed_markings.svg")
    svgWidget.setGeometry(50,50,400,400)
    svgWidget.show()"""


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
