import os
from PyQt5 import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Overlay(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        self.pixmap2 = QPixmap(os.path.join('img/airspeed_hand.svg'))

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(0)
        painter.drawPixmap(0, 0, self.pixmap2)
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
