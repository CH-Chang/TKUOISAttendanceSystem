from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime, timedelta

from ui.Ui_EditScheduleDialog import Ui_EditScheduleDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper
from utils.ShiftHelper import ShiftHelper

class EditScheduleDialog(QDialog):
    def __init__(self):
        super(EditScheduleDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initSQL()
        self.initInteraction()
        self.initOther()

    def initUI(self):
        self.ui = Ui_EditScheduleDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False
        self.ShiftHelper = ShiftHelper()

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.query.clicked.connect(self.queryClicked)
        self.ui.editOnTimeCheckIn.clicked.connect(self.editOnTimeCheckInClicked)
        self.ui.editOnTimeCheckOut.clicked.connect(self.editOnTimeCheckOutClicked)
        self.ui.editLate.clicked.connect(self.editLateClicked)
        self.ui.editExcused.clicked.connect(self.editExcusedClicked)
        self.ui.clearCheckIn.clicked.connect(self.clearCheckInClicked)
        self.ui.clearCheckOut.clicked.connect(self.clearCheckOutClicked)

    def loading(self):
        self.loadingDate()

    def loadingDate(self):
        now = datetime.now()

        self.ui.dateStart.setDate(QDate(now.year, now.month, now.day))
        self.ui.dateEnd.setDate(QDate(now.year, now.month, now.day))

    def query(self):
        startDate = self.ui.dateStart.date()
        endDate = self.ui.dateEnd.date()
        start = f'{startDate.year():04d}-{startDate.month():02d}-{startDate.day():02d}'
        end = f'{endDate.year():04d}-{endDate.month():02d}-{endDate.day():02d}'

        if datetime.strptime(start, "%Y-%m-%d") > datetime.strptime(end, "%Y-%m-%d"):
            dialog = MessageDialog("錯誤訊息", "查詢時間區間設定錯誤，請查核後重試")
            dialog.exec()
        else:
            schedules = self.SQLHelper.getScheduleDetailByDateInterval(start, end)

            result = []

            for schedule in schedules:
                scheduleStatus = self.ShiftHelper.getShiftStatus(schedule[4], schedule[1], schedule[8], schedule[9])
                scheduleCheckIn = ''
                scheduleCheckOut = ''
                if not schedule[8] is None:
                    scheduleCheckIn = schedule[8]
                if not schedule[9] is None:
                    scheduleCheckOut = schedule[9]

                result.append(
                    [schedule[0], f'{schedule[2]:03d}', schedule[3], schedule[1], schedule[5], schedule[7], scheduleCheckIn,
                     scheduleCheckOut, scheduleStatus])

            self.ui.loadingList(result)





    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def queryClicked(self):
        self.query()

    def editOnTimeCheckInClicked(self):
        if len(self.ui.listArea.selectedItems())!=0:
            scheduleId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)

            schedule = self.SQLHelper.getScheduleDetailWithShiftById(scheduleId)[0]

            dialog = MessageDialog("提示訊息", "請確認是否將該筆資料之簽到時間設定為準時")
            if dialog.exec():
                onTimeCheckIn = datetime.strptime(f'{schedule[1]} {schedule[6]}', "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)

                self.SQLHelper.updateScheduleCheckInById(onTimeCheckIn.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                self.query()
        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再執行操作")
            dialog.exec()


    def editOnTimeCheckOutClicked(self):

        if len(self.ui.listArea.selectedItems())!=0:
            scheduleId = self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole)

            schedule = self.SQLHelper.getScheduleDetailWithShiftById(scheduleId)[0]

            if schedule[12] is None:
                dialog = MessageDialog("錯誤訊息", "無法設定無簽到記錄之項目，請先設定簽到記錄")
                dialog.exec()
            else:
                dialog = MessageDialog("提示訊息", "請確認是否將該筆資料之簽退時間設定為準時")
                if dialog.exec():
                    onTimeCheckIn = datetime.strptime(f'{schedule[1]} {schedule[6]}', "%Y-%m-%d %H:%M:%S")
                    onTimeCheckOut = datetime.strptime(f'{schedule[1]} {schedule[7]}', "%Y-%m-%d %H:%M:%S")

                    if onTimeCheckIn > onTimeCheckOut:
                        onTimeCheckOut += timedelta(days=1)

                    self.SQLHelper.updateScheduleCheckOutById(onTimeCheckOut.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                    self.query()

        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再執行操作")
            dialog.exec()





    def editLateClicked(self):
        if len(self.ui.listArea.selectedItems())!=0:
            schedule = self.SQLHelper.getScheduleDetailWithShiftById(self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole))[0]

            dialog = MessageDialog("提示訊息", "請確認是否將該筆資料設為遲到")
            if dialog.exec():
                lateCheckIn = datetime.strptime(f'{schedule[1]} {schedule[6]}', "%Y-%m-%d %H:%M:%S")

                self.SQLHelper.updateScheduleCheckInById(lateCheckIn.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                self.query()
        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再執行操作")
            dialog.exec()



    def editExcusedClicked(self):
        if len(self.ui.listArea.selectedItems())!=0:
            schedule = self.SQLHelper.getScheduleDetailWithShiftById(self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole))[0]

            dialog = MessageDialog("提示訊息", "請確認是否將該筆資料設為早退")
            if dialog.exec():
                if schedule[12] is None:
                    dialog = MessageDialog("錯誤訊息", "無法設定無簽到記錄之項目，請先設定簽到記錄")
                    dialog.exec()
                else:
                    excusedCheckOut = datetime.strptime(f'{schedule[1]} {schedule[7]}', "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)

                    self.SQLHelper.updateScheduleCheckOutById(excusedCheckOut.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                    self.query()
        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再執行操作")
            dialog.exec()

    def clearCheckInClicked(self):
        if len(self.ui.listArea.selectedItems()) != 0:
            schedule = self.SQLHelper.getScheduleDetailWithShiftById(self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole))[0]

            if not schedule[13] is None:
                dialog = MessageDialog("錯誤訊息", "無法清除有簽退紀錄之簽到記錄，請先清除簽退紀錄")
                dialog.exec()
            else:
                dialog = MessageDialog("提示訊息", "請確認是否清除簽到紀錄")
                if dialog.exec():
                    self.SQLHelper.updateScheduleCheckInNullById(schedule[0])
                    self.query()
        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再執行操作")
            dialog.exec()

    def clearCheckOutClicked(self):
        if len(self.ui.listArea.selectedItems())!=0:
            schedule = self.SQLHelper.getScheduleDetailWithShiftById(self.ui.listArea.selectedItems()[0].data(0, Qt.UserRole))[0]

            dialog = MessageDialog("提示訊息", "請確認是否清除簽退紀錄")
            if dialog.exec():
                self.SQLHelper.updateScheduleCheckOutNullById(schedule[0])
                self.query()


        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇項目後再執行操作")
            dialog.exec()









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