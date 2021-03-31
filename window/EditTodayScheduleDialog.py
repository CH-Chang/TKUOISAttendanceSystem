from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

from ui.Ui_EditTodayScheduleDialog import Ui_EditTodayScheduleDialog

from window.MessageDialog import MessageDialog
from window.EditTodayScheduleCellDialog import EditTodayScheduleCellDialog

from utils.SQLHelper import SQLHelper
from utils.ShiftHelper import ShiftHelper


class EditTodayScheduleDialog(QDialog):
    def __init__(self):
        super(EditTodayScheduleDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_EditTodayScheduleDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False
        self.ShiftHelper = ShiftHelper()

    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.delete.clicked.connect(self.deleteClicked)
        self.ui.edit.clicked.connect(self.editClicked)
        self.ui.add.clicked.connect(self.addClicked)

    def loading(self):
        self.loadingTodaySchedule()

    def loadingTodaySchedule(self):
        now = datetime.now()

        schedules = self.SQLHelper.getScheduleDetailByDate(now.strftime("%Y-%m-%d"))
        result = []

        for schedule in schedules:
            scheduleStatus = self.ShiftHelper.getShiftStatus(schedule[4], schedule[3], schedule[8], schedule[9])
            result.append([schedule[0], f'{schedule[1]:03d}', schedule[2], schedule[5], schedule[7], schedule[8], schedule[9], scheduleStatus])

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
                scheduleId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
                self.SQLHelper.delScheduleById(scheduleId)

                self.loadingTodaySchedule()

    def editClicked(self):
        if len(self.ui.listArea.selectedItems()) == 0:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再進行相關操作")
            dialog.exec()
        else:
            scheduleId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)
            dialog = EditTodayScheduleCellDialog(scheduleId)
            if dialog.exec():
                self.loadingTodaySchedule()

    def addClicked(self):
        dialog = EditTodayScheduleCellDialog(None)
        if dialog.exec():
            self.loadingTodaySchedule()




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
