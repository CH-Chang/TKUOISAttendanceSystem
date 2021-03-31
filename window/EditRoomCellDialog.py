from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

from ui.Ui_EditRoomCellDialog import Ui_EditRoomCellDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper

class EditRoomCellDialog(QDialog):

    def __init__(self, roomId):
        super(EditRoomCellDialog, self).__init__()
        self.init(roomId)
        self.loading()


    def init(self, roomId):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()
        self.initValue(roomId)

    def initUI(self):
        self.ui = Ui_EditRoomCellDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initValue(self, roomId):
        self.roomId = roomId


    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)
        self.ui.nameLineEdit.returnPressed.connect(self.nameLineEditReturnPressed)


    def loading(self):
        self.loadingData()
        self.loadingData()

    def loadingData(self):
        if not self.roomId is None:
            room = self.SQLHelper.getRoomById(self.roomId)[0]
            self.ui.nameLineEdit.setText(room[1])





    def loadingFocus(self):
        self.ui.nameLineEdit.setFocus(True)



    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):


        name = self.ui.nameLineEdit.text()


        if name=='':
            dialog = MessageDialog("錯誤訊息", "請確認表單內容填寫完整")
            dialog.exec()
        else:
            if self.roomId is None:
                dialog = MessageDialog("提示訊息", "請確認是否新增該筆實習室資料")
                if dialog.exec():

                    if self.isDuplicatedRoom(name):
                        dialog = MessageDialog("錯誤訊息", "實習室名稱重複，請確認後重試")
                        dialog.exec()
                    else:
                        self.SQLHelper.newRoom(name)
                        self.SQLHelper.close()
                        self.accept()


            else:
                dialog = MessageDialog("提示訊息", "請確認是否修改該筆實習室資料")
                if dialog.exec():
                    if self.isDuplicatedRoom(name):
                        dialog = MessageDialog("錯誤訊息", "實習室名稱重複，請確認後重試")
                        dialog.exec()
                    else:
                        self.SQLHelper.updateRoomById(self.roomId, name)
                        self.SQLHelper.close()
                        self.accept()



    def nameLineEditReturnPressed(self):
        self.comfirmClicked()

    def isDuplicatedRoom(self, roomName):
        rooms = self.SQLHelper.getAllRoom()

        for room in rooms:
            if room[1] == roomName:
                return True

        return False





















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