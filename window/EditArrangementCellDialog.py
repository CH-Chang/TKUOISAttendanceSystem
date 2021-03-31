from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui.Ui_EditArrangementCellDialog import Ui_EditArrangementCellDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper


class EditArrangementCellDialog(QDialog):
    def __init__(self, arrangementId):
        super(EditArrangementCellDialog, self).__init__()
        self.init()
        self.loading(arrangementId)

    def init(self):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_EditArrangementCellDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)


    def loading(self, arrangementId):
        self.loadingWeek()
        self.loadingShift()
        self.loadingRoom()
        self.loadingPeriod()
        self.loadingStaff()
        self.loadingArrangement(arrangementId)

    def loadingWeek(self):
        result = [["星期一", 0], ["星期二", 1], ["星期三", 2], ["星期四", 3], ["星期五", 4], ["星期六", 5], ["星期日", 6]]
        self.ui.loadingWeek(result)

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

    def loadingPeriod(self):
        periods = self.SQLHelper.getPeriodNotVacation()
        result = []

        for period in periods:
            result.append([period[1], period[0]])

        self.ui.loadingPeriod(result)

    def loadingStaff(self):
        staffs = self.SQLHelper.getAllStaff()
        result = []

        for staff in staffs:
            result.append([f'{staff[0]:03d}', staff[2], staff[0]])

        self.ui.loadingStaff(result)

    def loadingArrangement(self, arrangementId):
        self.arrangementId = arrangementId
        if not arrangementId is None:
            arrangement = self.SQLHelper.getArrangementDetailById(arrangementId)[0]

            weekTrans = {0:"星期一", 1:"星期二", 2:"星期三", 3:"星期四", 4:"星期五", 5:"星期六", 6: "星期日"}

            self.ui.weekSelection.setCurrentText(weekTrans[arrangement[3]])
            self.ui.shiftSelection.setCurrentText(arrangement[5])
            self.ui.roomSelection.setCurrentText(arrangement[7])
            self.ui.periodSelection.setCurrentText(arrangement[9])
            self.ui.staffSelection.setCurrentText(f'{arrangement[1]:03d} {arrangement[2]}')


    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):

        week = self.ui.weekSelection.currentData(Qt.UserRole)
        shiftId = self.ui.shiftSelection.currentData(Qt.UserRole)
        roomId = self.ui.roomSelection.currentData(Qt.UserRole)
        periodId = self.ui.periodSelection.currentData(Qt.UserRole)
        staffId = self.ui.staffSelection.currentData(Qt.UserRole)

        if self.arrangementId is None:
            dialog = MessageDialog("提示訊息", "請確認是否新增該筆排班資料")
            if dialog.exec():
                self.SQLHelper.newArrangement(staffId, week, shiftId, roomId, periodId)
                self.accept()
        else:
            dialog = MessageDialog("提示訊息", "請確認是否修改該筆排班資料")
            if dialog.exec():
                self.SQLHelper.updateArrangementById(self.arrangementId, staffId, week, shiftId, roomId, periodId)
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