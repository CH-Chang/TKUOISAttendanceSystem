from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.Ui_MessageDialog import Ui_MessageDialog

class MessageDialog(QDialog):

    def __init__(self, title, message):
        super(MessageDialog, self).__init__()
        self.init(title, message)
        self.loading()

    def init(self, title, message):
        self.initValue(title, message)
        self.initUI()
        self.initInteraction()
        self.initOther()

    def initValue(self, title, message):
        if not title is None:
            self.title = title
        else:
            self.title = "提示訊息"
        if not message is None:
            self.message = message
        else:
            self.message = ""

    def initUI(self):
        self.ui = Ui_MessageDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)

    def initOther(self):
        self.moveFlag = False

    def loading(self):
        self.loadingTitle()
        self.loadingMessage()

    def loadingTitle(self):
        self.ui.loadingTitle(self, self.title)

    def loadingMessage(self):
        self.ui.loadingMessage(self.message)

    def setTitle(self, title):
        self.title = title
        self.loadingTitle()

    def setMessage(self, message):
        self.message = message
        self.loadingMessage()

    def dialogNavCloseClicked(self):
        self.reject()

    def cancelClicked(self):
        self.reject()

    def comfirmClicked(self):
        self.accept()

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