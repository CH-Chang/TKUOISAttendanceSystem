from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from win32event import CreateMutex
from winerror import ERROR_ALREADY_EXISTS
from win32api import GetLastError

from window.Splash import Splash

from utils.SvgHelper import SvgHelper
from icon.svg import logoIcon

import sys

import globals




globals.mutex = CreateMutex(None, False, "TKUInfoCenterClient")
if GetLastError() == ERROR_ALREADY_EXISTS:
    sys.exit(0)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(SvgHelper.getQPixmapFromBytes(logoIcon, QSize(512,512))))
globals.window = Splash()
globals.window.show()
sys.exit(app.exec_())




