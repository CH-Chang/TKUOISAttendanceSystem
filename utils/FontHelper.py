from base64 import b64decode
from PyQt5.QtGui import *

from font.otf import NotoSansTCRegular

class FontHelper:

    @staticmethod
    def initNotoSansTCRegular() -> None:

        rawFont = b64decode(NotoSansTCRegular)

        fontId = QFontDatabase.addApplicationFontFromData(rawFont)