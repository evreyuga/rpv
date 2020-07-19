from pyqtgraph import PlotWidget, ImageItem
from PyQt5.QtCore import QRectF, pyqtSlot, QCoreApplication
import numpy as np


class Dna2DWidget(PlotWidget):

    def __init__(self):
        super(Dna2DWidget, self).__init__()
        # M.B. plot add to params
        self.setXRange(-60, 60)
        self.setYRange(-60, 60)
        self.img = ImageItem()
        self.addItem(self.img)
        _translate = QCoreApplication.translate
        self.setLabels(title=_translate("Dna2DWidget", "2D DNA"),
                       left=_translate("Dna2DWidget", "Elevation, °"),
                       bottom=_translate("Dna2DWidget", "Azimuth, °"))
        self.setLogMode()

    @pyqtSlot()
    def onDataChaged(self):
        sender = self.sender()
        self.img.setImage(sender.data)
        self.img.setRect(self.__ensure_rect(np.shape(sender.data)))

    # TODO: rewrite for accuracy
    def __ensure_rect(self, shape):
        x_offset = 120. / (shape[0]-1) / 2
        y_offset = 120. / (shape[1]-1) / 2
        return QRectF(-60 - x_offset, -60 - y_offset, 120 + x_offset * 2, 120 + y_offset * 2)





