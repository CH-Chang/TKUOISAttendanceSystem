from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.Ui_EditRoomDialog import Ui_EditRoomDialog

from window.MessageDialog import MessageDialog
from window.EditRoomCellDialog import EditRoomCellDialog

from utils.SQLHelper import SQLHelper

class EditRoomDialog(QDialog):
    def __init__(self):
        super(EditRoomDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_EditRoomDialog()
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
        self.loadingRoom()

    def loadingRoom(self):
        rooms = self.SQLHelper.getAllRoom()

        self.ui.loadingList(rooms)


    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def deleteClicked(self):
        if len(self.ui.listArea.selectedItems()) == 0:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再進行相關操作")
            dialog.exec()
        else:
            dialog = MessageDialog("提示訊息", "請確認是否刪除該項實習室資料及其關聯的所有班表資訊")
            if dialog.exec():
                roomId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
                self.SQLHelper.delRoomById(roomId)
                self.loadingRoom()


    def editClicked(self):
        if len(self.ui.listArea.selectedItems()) == 0:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再進行相關操作")
            dialog.exec()
        else:
            roomId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
            dialog = EditRoomCellDialog(roomId)
            if dialog.exec():
                self.loadingRoom()


    def addClicked(self):
        dialog = EditRoomCellDialog(None)
        if dialog.exec():
            self.loadingRoom()




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
