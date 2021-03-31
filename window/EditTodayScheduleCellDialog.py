from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

from ui.Ui_EditTodayScheduleCellDialog import Ui_EditTodayScheduleCellDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper


class EditTodayScheduleCellDialog(QDialog):
    def __init__(self, scheduleId):
        super(EditTodayScheduleCellDialog, self).__init__()
        self.init()
        self.loading(scheduleId)

    def init(self):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_EditTodayScheduleCellDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)


    def loading(self, scheduleId):
        self.loadingShift()
        self.loadingRoom()
        self.loadingStaff()
        self.loadingSchedule(scheduleId)


    def loadingShift(self):
        shifts = self.SQLHelper.getAllShift()
        result = []

        for shift in shifts:
            result.append([shift[1], shift[0]])

        self.ui.loadingShift(result)

    def loadingRoom(self):
        rooms = self.SQLHelper.getAllRoom()
        result = []

        for room in rooms:
            result.append([room[1], room[0]])

        self.ui.loadingRoom(result)

    def loadingStaff(self):
        staffs = self.SQLHelper.getAllStaff()
        result = []

        for staff in staffs:
            result.append([f'{staff[0]:03d}', staff[2], staff[0]])

        self.ui.loadingStaff(result)

    def loadingSchedule(self, scheduleId: int):
        self.scheduleId = scheduleId
        if not scheduleId is None:

            schedule = self.SQLHelper.getScheduleDetailById(scheduleId)[0]

            self.ui.shiftSelection.setCurrentText(schedule[5])
            self.ui.roomSelection.setCurrentText(schedule[7])
            self.ui.staffSelection.setCurrentText(f'{schedule[1]:03d} {schedule[2]}')


    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):

        shiftId = self.ui.shiftSelection.currentData(Qt.UserRole)
        roomId = self.ui.roomSelection.currentData(Qt.UserRole)
        staffId = self.ui.staffSelection.currentData(Qt.UserRole)
        date = datetime.now().strftime("%Y-%m-%d")

        if self.scheduleId is None:
            dialog = MessageDialog("提示訊息", "請確認是否新增該筆排班資料")
            if dialog.exec():
                self.SQLHelper.newSchedule(date, staffId, shiftId, roomId)
                self.accept()
        else:
            dialog = MessageDialog("提示訊息", "請確認是否修改該筆排班資料")
            if dialog.exec():
                self.SQLHelper.updateScheduleById(staffId, shiftId, roomId, self.scheduleId)
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