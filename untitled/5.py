import os
import sys
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel


class Myform(QWidget):

    def __init__(self):
        super(Myform, self).__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        self.pixmap = QPixmap(os.path.join('airspeed_markings.svg'))
        self.pixmap2 = QPixmap(os.path.join('airspeed_hand.svg'))
        lbl = QLabel(self)
        lbl.setPixmap(self.pixmap)  # 设置标签内容图片

        hbox.addWidget(lbl)
        self.setLayout(hbox)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(600, 200)
        painter.rotate(150)  # 顺时针旋转150度
        painter.drawPixmap(0, 0, 400, 400, self.pixmap2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Myform()
    w.show()
    sys.exit(app.exec_())
