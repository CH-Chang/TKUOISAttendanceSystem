from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from window.MessageDialog import MessageDialog
from ui.Ui_AuthDialog import Ui_AuthDialog
from utils.SQLHelper import SQLHelper
from utils.HMACSHA256Helper import HMACSHA256Helper

class AuthDialog(QDialog):

    def __init__(self):
        super(AuthDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initInteraction()
        self.initOther()
        self.initSQL()

    def initUI(self):
        self.ui = Ui_AuthDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.passwordLineEdit.returnPressed.connect(self.comfirmClicked)

    def initOther(self):
        self.moveFlag = False

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def loading(self):
        self.loadingFocus()

    def loadingFocus(self):
        self.ui.passwordLineEdit.setFocus(True)

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):
        password = self.ui.passwordLineEdit.text()
        hashPassword = HMACSHA256Helper.HMACSHA256Hash(password)
        sysPassword = self.SQLHelper.getPWD()

        if hashPassword==sysPassword:
            self.SQLHelper.close()
            self.accept()
        else:
            self.hide()
            dialog = MessageDialog("錯誤提示", "管理員密碼錯誤，請重試")
            dialog.exec()
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