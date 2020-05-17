from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.init_plot()#打开App时可以初始化图片
        # self.plot()

    def plot(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def init_plot(self, title, unit, time):
        self.title = title
        self.unit = unit
        self.time = time
        self.axes.set_title(self.title)
        self.axes.set_ylabel(self.unit)
        self.axes.set_xlabel(self.time)
        """
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)
        """

    def update_figure(self, x, y):
        # x = np.linspace(0, 10, 10)
        # y = [random.randint(0, 10) for i in range(10)]
        # xx = np.linspace(0, 10)
        # f = interpolate.interp1d(x, y, 'quadratic')  # 产生插值曲线的函数
        # yy = f(xx)
        self.axes.cla()
        self.axes.set_title(self.title)
        self.axes.set_ylabel(self.unit)
        self.axes.set_xlabel(self.time)
        self.axes.plot(x, y)
        self.draw()

    def outputImage(self,title):
        self.fig.savefig(title+'.png')
