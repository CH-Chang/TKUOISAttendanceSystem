from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.Ui_EditArrangementDialog import Ui_EditArrangementDialog

from window.MessageDialog import MessageDialog
from window.EditArrangementCellDialog import EditArrangementCellDialog

from utils.SQLHelper import SQLHelper


class EditArrangementDialog(QDialog):
    def __init__(self):
        super(EditArrangementDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_EditArrangementDialog()
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
        self.loadingArrangement()

    def loadingArrangement(self):
        arrangements = self.SQLHelper.getAllArrangementDetail()

        weekTrans = {0:"星期一", 1:"星期二", 2:"星期三", 3:"星期四", 4:"星期五", 5:"星期六", 6: "星期日"}
        result = []

        for arrangement in arrangements:
            result.append([arrangement[0], weekTrans[arrangement[3]], f'{arrangement[1]:03d}', arrangement[2], arrangement[5], arrangement[7], arrangement[9]])

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
            dialog = MessageDialog("提示訊息", "請確認是否刪除該筆排班資料")
            if dialog.exec():
                arrangementId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
                self.SQLHelper.delArrangementById(arrangementId)

                self.loadingArrangement()

    def editClicked(self):
        if len(self.ui.listArea.selectedItems()) == 0:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再進行相關操作")
            dialog.exec()
        else:
            arrangementId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
            dialog = EditArrangementCellDialog(arrangementId)
            if dialog.exec():
                self.loadingArrangement()

    def addClicked(self):
        dialog = EditArrangementCellDialog(None)
        if dialog.exec():
            self.loadingArrangement()




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
