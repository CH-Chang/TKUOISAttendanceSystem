from PyQt5.Qt import *
from PyQt5.QtSvg import *
from PyQt5.QtGui import *

from base64 import b64decode

class SvgHelper:
    
    @staticmethod
    def getQPixmapFromBytes(bytes, size):
        img = b64decode(bytes)
        render = QSvgRenderer(img)
        frame = QImage(size.width(), size.height(), QImage.Format_ARGB32)
        painter = QPainter(frame)

        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        frame.fill(Qt.transparent)
        render.render(painter)
        output = QPixmap.fromImage(frame)

        del painter

        return output