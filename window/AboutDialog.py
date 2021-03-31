from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.Ui_AboutDialog import Ui_AboutDialog

class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog, self).__init__()
        self.init()

    def init(self):
        self.initUI()
        self.initInteraction()
        self.initOther()

    def initUI(self):
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)

    def initOther(self):
        self.moveFlag = False



    def dialogNavCloseClicked(self):
        self.reject()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.moveFlag = False
        self.setCursor(Qt.ArrowCursor)

