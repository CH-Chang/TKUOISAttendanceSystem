from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from window.MessageDialog import MessageDialog
from ui.Ui_ChgAuthDialog import Ui_ChgAuthDialog
from utils.SQLHelper import SQLHelper
from utils.HMACSHA256Helper import HMACSHA256Helper

class ChgAuthDialog(QDialog):

    def __init__(self):
        super(ChgAuthDialog, self).__init__()
        self.init()

    def init(self):
        self.initUI()
        self.initInteraction()
        self.initOther()
        self.initSQL()

    def initUI(self):
        self.ui = Ui_ChgAuthDialog()
        self.ui.setupUi(self)

    def initOther(self):
        self.moveFlag = False

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.checkPasswordLineEdit.returnPressed.connect(self.comfirmClicked)
        self.ui.passwordLineEdit.returnPressed.connect(self.passwordLineEditReturnPressed)



    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()


    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):
        password = self.ui.passwordLineEdit.text()
        checkPassword = self.ui.checkPasswordLineEdit.text()

        if password!=checkPassword:
            self.hide()
            dialog = MessageDialog("錯誤提示", "兩次密碼輸入不相同，請重試")
            dialog.exec()
            self.reject()
        else:
            hashPassword = HMACSHA256Helper.HMACSHA256Hash(password)
            self.SQLHelper.updatePWD(hashPassword)
            self.hide()
            dialog = MessageDialog("提示訊息", "密碼修改成功")
            dialog.exec()
            self.accept()

    def passwordLineEditReturnPressed(self):
        self.ui.checkPasswordLineEdit.setFocus(True)




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