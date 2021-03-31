from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.Ui_EditStaffDialog import Ui_EditStaffDialog

from window.MessageDialog import MessageDialog
from window.EditStaffCellDialog import EditStaffCellDialog

from utils.SQLHelper import SQLHelper


class EditStaffDialog(QDialog):
    def __init__(self):
        super(EditStaffDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_EditStaffDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.delete.clicked.connect(self.deleteClicked)
        self.ui.edit.clicked.connect(self.editClicked)
        self.ui.add.clicked.connect(self.addClicked)

    def loading(self):
        self.loadingStaff()

    def loadingStaff(self):
        staffs = self.SQLHelper.getAllStaff()

        result = []

        for staff in staffs:
            result.append([staff[0], f'{staff[0]:03d}', staff[1], staff[2]])

        self.ui.loadingList(result)

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def deleteClicked(self):

        if len(self.ui.listArea.selectedItems())==0:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再進行相關操作")
            dialog.exec()
        else:
            dialog = MessageDialog("提示訊息", "刪除工讀生將一併刪除其紀錄資料及其班表資料，請再次確認")
            if dialog.exec():
                staffId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
                self.SQLHelper.delStaffById(staffId)

                self.loadingStaff()

    def editClicked(self):
        if len(self.ui.listArea.selectedItems()) == 0:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再進行相關操作")
            dialog.exec()
        else:
            staffId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
            dialog = EditStaffCellDialog(staffId)
            if dialog.exec():
                self.loadingStaff()

    def addClicked(self):

        dialog = EditStaffCellDialog(None)
        if dialog.exec():
            self.loadingStaff()




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
