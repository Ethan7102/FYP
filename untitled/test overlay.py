# https://github.com/KubaO/stackoverflown/tree/master/questions/python-overlay-49920532
import os
from time import sleep

from PyQt5 import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

rotate = 0

class Overlay(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        self.pixmap2 = QPixmap(os.path.join('airspeed_hand.svg'))

        pointer = QPolygonF()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()
        painter.translate(0,0)
        painter.rotate(10)
        painter.drawPixmap(pointer,self.pixmap2)
        painter.restore()




class Filter(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.m_overlay = None
        self.m_overlayOn = None

    def eventFilter(self, w, event):
        if w.isWidgetType():
            if event.type() == QEvent.Paint:
                if not self.m_overlay:
                    m_overlay = Overlay(w.parentWidget());
                    m_overlay.setGeometry(w.geometry());
                    m_overlayOn = w;
                    m_overlay.show();
            elif event.type() == QEvent.Resize:
                if self.m_overlay and self.m_overlayOn is w:
                    self.m_overlay.setGeometry(w.geometry());
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    filter = Filter()
    window = QWidget()
    layout = QHBoxLayout(window)
    pixmap = QPixmap(os.path.join('airspeed_markings.svg'))
    label = QLabel()
    label.setPixmap(pixmap)
    label.installEventFilter(filter)
    layout.addWidget(label)
    window.setMinimumSize(400, 400)
    window.show()
    app.exec_()
