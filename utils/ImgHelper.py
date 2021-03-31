from base64 import b64decode

import numpy
import cv2

from PyQt5.QtGui import QImage


class ImgHelper:

    @staticmethod
    def getImageQtfromBytes(bytes):
        imageString = b64decode(bytes)
        image = cv2.imdecode(numpy.fromstring(imageString, numpy.uint8), cv2.IMREAD_COLOR)
        height, width, depth = image.shape
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imageQT = QImage(image.data, width, height, width*depth, QImage.Format_RGB888)
        return imageQT

