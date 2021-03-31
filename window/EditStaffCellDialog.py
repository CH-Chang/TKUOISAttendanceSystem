from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.Ui_EditStaffCellDialog import Ui_EditStaffCellDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper

class EditStaffCellDialog(QDialog):

    def __init__(self, staffId):
        super(EditStaffCellDialog, self).__init__()
        self.init(staffId)
        self.loading()


    def init(self, staffId):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()
        self.initValue(staffId)

    def initUI(self):
        self.ui = Ui_EditStaffCellDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initValue(self, staffId):
        self.staffId = staffId


    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)

    def loading(self):
        if not self.staffId is None:
            staff = self.SQLHelper.getStaffById(self.staffId)[0]

            self.ui.staffNumLineEdit.setText(str(staff[0]))
            self.ui.staffNumLineEdit.setEnabled(False)
            self.ui.stuNumLineEdit.setText(staff[1])
            self.ui.nameLineEdit.setText(staff[2])

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):

        staffNum = self.ui.staffNumLineEdit.text()
        stuNum = self.ui.stuNumLineEdit.text()
        name = self.ui.nameLineEdit.text()

        if staffNum == '' or stuNum == '' or name =='':
            dialog = MessageDialog("錯誤訊息", "請確認表單資料填寫完整")
            dialog.exec()
        else:
            staffNum = int(staffNum)
            if self.staffId is None:
                staffs = self.SQLHelper.getStaffById(staffNum)
                if len(staffs) != 0:
                    dialog = MessageDialog("錯誤訊息", f'已有工讀生編號{staffNum}號的工讀生，請查核後重試')
                    dialog.exec()
                else:
                    dialog = MessageDialog("提示訊息", "請確認是否新增工讀生")
                    if dialog.exec():
                        self.SQLHelper.newStaff(staffNum, stuNum, name)
                        self.accept()
            else:
                dialog = MessageDialog("提示訊息", "請確認是否修改工讀生")
                if dialog.exec():
                    self.SQLHelper.updateStaffById(staffNum, stuNum, name)
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