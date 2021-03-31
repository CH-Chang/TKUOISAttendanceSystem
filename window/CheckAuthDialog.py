from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from window.MessageDialog import MessageDialog
from ui.Ui_CheckAuthDialog import Ui_CheckAuthDialog
from utils.SQLHelper import SQLHelper
from utils.HMACSHA256Helper import HMACSHA256Helper

class CheckAuthDialog(QDialog):

    def __init__(self, staffNum):
        super(CheckAuthDialog, self).__init__()
        self.init(staffNum)
        self.loadingFocus()

    def init(self, staffNum):
        self.initValue(staffNum)
        self.initUI()
        self.initInteraction()
        self.initOther()
        self.initSQL()

    def initValue(self, staffNum):
        self.staffNum = staffNum

    def initUI(self):
        self.ui = Ui_CheckAuthDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.stuNumLineEdit.returnPressed.connect(self.comfirmClicked)

    def initOther(self):
        self.moveFlag = False

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def loading(self):
        self.loadingFocus()

    def loadingFocus(self):
        self.ui.stuNumLineEdit.setFocus(True)


    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):

        staff = self.SQLHelper.getStaffById(self.staffNum)[0]

        if self.ui.stuNumLineEdit.text() == staff[1]:
            self.accept()
        else:
            self.hide()
            dialog = MessageDialog("錯誤提示", "操作人員驗證錯誤，請重試")
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