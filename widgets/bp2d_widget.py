from pyqtgraph import PlotWidget, ImageItem, ColorMap, GradientLegend
from pyqtgraph.graphicsItems.GradientEditorItem import Gradients
from PyQt5.QtCore import QRectF, pyqtSlot, QCoreApplication
import numpy as np


class Bp2DWidget(PlotWidget):

    def __init__(self):
        super(Bp2DWidget, self).__init__()
        # M.B. plot add to params
        self.setXRange(-60, 60)
        self.setYRange(-60, 60)
        self.img = ImageItem()
        self.addItem(self.img)
        _translate = QCoreApplication.translate
        self.setLabels(title=_translate("Bp2DWidget", "Beam pattern"),
                       left=_translate("Bp2DWidget", "Elevation, °"),
                       bottom=_translate("Bp2DWidget", "Azimuth, °"))
        self.setLogMode()
        colormap = ColorMap(*zip(*Gradients["bipolar"]["ticks"]))
        self.img.setLookupTable(colormap.getLookupTable())
        #gradient_legend = GradientLegend(10, 10)
        #self.addItem(gradient_legend)

    @pyqtSlot()
    def on_data_changed(self):
        sender = self.sender()
        self.img.setImage(np.rot90(sender.data, -1))
        self.img.setRect(self.__ensure_rect(np.shape(sender.data)))

    def __ensure_rect(self, shape):
        x_offset = 120. / (shape[0]-1) / 2
        y_offset = 120. / (shape[1]-1) / 2
        return QRectF(-60 - x_offset, 60 + y_offset, 120 + x_offset * 2, -120 - y_offset * 2)





