# -*-coding:utf-8-*-

import sys
from datetime import datetime

from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtGui import QColor, QPalette, QBrush, QPixmap, QPolygon, QPainter
from PyQt5.QtWidgets import QWidget, QApplication, QAction


class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)

        self.checktime()

        self.hourColor = QColor(127, 0, 127);
        self.minuteColor = QColor(0, 127, 127, 191)
        self.secondColor = QColor(127, 127, 0, 120)

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

    def handChange(self):
        self.side = min(self.width(), self.height())
        self.hand = (max(self.side / 200, 4), max(self.side / 100, 8), max(self.side / 40, 30))
        self.hourHand = QPolygon(
            [QPoint(self.hand[0], self.hand[1]), QPoint(-self.hand[0], self.hand[1]), QPoint(0, -self.hand[2])])
        self.minuteHand = QPolygon(
            [QPoint(self.hand[0], self.hand[1]), QPoint(-self.hand[0], self.hand[1]), QPoint(0, -self.hand[2] * 1.6)])
        self.secondHand = QPolygon([QPoint(self.hand[0], self.hand[1]), QPoint(-self.hand[0], self.hand[1]),
                                    QPoint(0, -self.hand[2] * 1.6 * 1.6)])

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
        qp.setBrush(self.hourColor)
        qp.save()
        qp.rotate(30.0 * ((self.time.hour + self.time.minute / 60.0)))
        qp.drawConvexPolygon(self.hourHand)
        qp.restore()

        qp.setPen(Qt.NoPen)
        qp.setBrush(self.minuteColor)
        qp.save()

        qp.rotate(6.0 * ((self.time.minute + (self.time.second) / 60.0)))
        qp.drawConvexPolygon(self.minuteHand)
        qp.restore()

        qp.setPen(Qt.NoPen)
        qp.setBrush(self.secondColor)
        qp.save()
        qp.rotate(6.0 * (self.time.second))
        qp.drawConvexPolygon(self.secondHand)
        qp.restore()

    def checktime(self):
        self.time = datetime.now()
        self.hour = self.time.hour
        self.minute = self.time.minute
        self.second = self.time.second

    # 拖拽
    def mouseReleaseEvent(self, e):
        if self.rightButton == True:
            self.rightButton = False

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self.dragPos)
            e.accept()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.dragPos = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()
        if e.button() == Qt.RightButton and self.rightButton == False:
            self.rightButton = True


def main():
    app = QApplication(sys.argv)
    palette = QPalette()

    brush = QBrush(QColor(0, 0, 0, 0), QPixmap("clock.png"))
    palette.setBrush(QPalette.Window, brush)
    clock = Clock()
    clock.setPalette(palette)
    clock.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
