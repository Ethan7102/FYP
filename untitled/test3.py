from datetime import datetime
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPolygon, QColor


class ArrowWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # since the widget will not be added to a layout, ensure
        # that it has a fixed size (otherwise it'll use QWidget default size)
        #self.setFixedSize(400, 400)
        self.blurRadius = 20
        self.xO = 0
        self.yO = 20
        shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=self.blurRadius, xOffset=self.xO, yOffset=self.yO)
        self.setGraphicsEffect(shadow)

        self.hourColor = QColor(127, 0, 127);
        self.minuteColor = QColor(0, 127, 127, 191)
        self.secondColor = QColor(127, 127, 0, 120)
        self.airspeedHandColor = QColor('white');

        self.initUI()

        print(self.width(), self.height())

        # create pen and brush colors for painting
    """    self.currentPen = self.normalPen = QtGui.QPen(QtCore.Qt.black)
        self.hoverPen = QtGui.QPen(QtCore.Qt.darkGray)
        self.currentBrush = self.normalBrush = QtGui.QColor(QtCore.Qt.transparent)
        self.hoverBrush = QtGui.QColor(128, 192, 192, 128)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        # move the widget based on its position and "delta" of the coordinates
        # where it was clicked. Be careful to use button*s* and not button
        # within mouseMoveEvent
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.mousePos)

    def enterEvent(self, event):
        self.currentPen = self.hoverPen
        self.currentBrush = self.hoverBrush
        self.update()

    def leaveEvent(self, event):
        self.currentPen = self.normalPen
        self.currentBrush = self.normalBrush
        self.update()"""

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
        qp = QtGui.QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        qp.begin(self)
        self.draw(event, qp)
        qp.end()
        # painting is not based on "pixels", to get accurate results
        # translation of .5 is required, expecially when using 1 pixel lines
        """qp.translate(.5, .5)
        # painting rectangle is always 1px smaller than the actual size
        rect = self.rect().adjusted(0, 0, -1, -1)
        qp.setPen(self.currentPen)
        qp.setBrush(self.currentBrush)
        # draw an ellipse smaller than the widget
        qp.drawEllipse(rect.adjusted(25, 25, -25, -25))
        # draw arrow lines based on the center; since a QRect center is a QPoint
        # we can add or subtract another QPoint to get the new positions for
        # top-left, right and bottom left corners
        qp.drawLine(rect.center() + QtCore.QPoint(-25, -50), rect.center() + QtCore.QPoint(25, 0))
        qp.drawLine(rect.center() + QtCore.QPoint(25, 0), rect.center() + QtCore.QPoint(-25, 50))"""

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


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        """self.setLayout(layout)
        self.button = QtWidgets.QPushButton('button')
        layout.addWidget(self.button, 0, 0)
        self.label = QtWidgets.QLabel('label')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label, 0, 1)"""
        label = RotateMe(alignment=QtCore.Qt.AlignCenter)
        img_path = os.path.join('airspeed_markings.svg')
        label.set_pixmap(QtGui.QPixmap(img_path))
        layout.addWidget(label)
        # create a frame that uses as much space as possible
        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(self.frame.StyledPanel|self.frame.Raised)
        self.frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # add it to the layout, ensuring it spans all rows and columns
        layout.addWidget(self.frame, 0, 0, layout.rowCount(), layout.columnCount())
        # "lower" the frame to the bottom of the widget's stack, otherwise
        # it will be "over" the other widgets, preventing them to receive
        # mouse events
        self.frame.lower()
        self.resize(400,400)
        # finally, create your widget with a parent, *without* adding to a layout
        self.arrowWidget = ArrowWidget(self)
        # now you can place it wherever you want
        self.arrowWidget.move(220, 140)

class RotateMe(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(RotateMe, self).__init__(*args, **kwargs)
        self._pixmap = QtGui.QPixmap()
        self._animation = QtCore.QVariantAnimation(
            self,
            startValue=0.0,
            endValue=360.0,
            duration=1000,
            valueChanged=self.on_valueChanged
        )

    def set_pixmap(self, pixmap):
        self._pixmap = pixmap
        self.setPixmap(self._pixmap)

    def start_animation(self):
        if self._animation.state() != QtCore.QAbstractAnimation.Running:
            self._animation.start()

    @QtCore.pyqtSlot(QtCore.QVariant)
    def on_valueChanged(self, value):
        t = QtGui.QTransform()
        t.rotate(value)
        self.setPixmap(self._pixmap.transformed(t))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    testWidget = MainWidget()
    testWidget.show()
    sys.exit(app.exec_())
