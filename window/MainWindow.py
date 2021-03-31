from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime, timedelta
from calendar import monthrange
from win32api import CloseHandle

from ui.Ui_MainWindow import Ui_MainWindow

from window.ImportStaffDialog import ImportStaffDialog
from window.ImportArrangementDialog import ImportArrangementDialog
from window.AuthDialog import AuthDialog
from window.CheckAuthDialog import CheckAuthDialog
from window.ChgAuthDialog import ChgAuthDialog
from window.MessageDialog import MessageDialog
from window.IntervalDialog import IntervalDialog
from window.NoncancelableDialog import NoncancelableDialog
from window.EditScheduleDialog import EditScheduleDialog
from window.EditStaffDialog import EditStaffDialog
from window.EditVacationDialog import EditVacationDialog
from window.EditArrangementDialog import EditArrangementDialog
from window.EditShiftDialog import EditShiftDialog
from window.EditTodayScheduleDialog import EditTodayScheduleDialog
from window.EditRoomDialog import EditRoomDialog
from window.AboutDialog import AboutDialog

from utils.SQLHelper import SQLHelper
from utils.ShiftHelper import ShiftHelper

import xlwings as xw
import os

import globals


class MainWindow(QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initInteraction()
        self.initSQL()
        self.initTherad()
        self.initOther()

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.adminView.clicked.connect(self.adminViewClicked)
        self.ui.windowNavClose.clicked.connect(self.windowNavCloseClicked)
        self.ui.windowNavMaximize.clicked.connect(self.windowNavMaximizeClicked)
        self.ui.windowNavMinimize.clicked.connect(self.windowNavMinimizeClicked)
        self.ui.importStaff.clicked.connect(self.importStaffClicked)
        self.ui.importSemester.clicked.connect(self.importSemesterClicked)
        self.ui.importMidterm.clicked.connect(self.importMidtermClicked)
        self.ui.importFinal.clicked.connect(self.importFinalClicked)
        self.ui.importSummer.clicked.connect(self.importSummberClicked)
        self.ui.importWinter.clicked.connect(self.importWinterClicked)
        self.ui.changePassword.clicked.connect(self.changePasswordClicked)
        self.ui.switchLeft.clicked.connect(self.switchLeftClicked)
        self.ui.switchRight.clicked.connect(self.switchRightClicked)
        self.ui.exportInterval.clicked.connect(self.exportIntervalClicked)
        self.ui.exportMonth.clicked.connect(self.exportMonthClicked)
        self.ui.exportLastMonth.clicked.connect(self.exportLastMonthClicked)
        self.ui.editSchedule.clicked.connect(self.editScheduleClicked)
        self.ui.editStaff.clicked.connect(self.editStaffClicked)
        self.ui.editArrangement.clicked.connect(self.editArrangementClicked)
        self.ui.editVacation.clicked.connect(self.editVacationClicked)
        self.ui.editShift.clicked.connect(self.editShiftClicked)
        self.ui.editRoom.clicked.connect(self.editRoomClicked)
        self.ui.editTodaySchedule.clicked.connect(self.editTodayScheduleClicked)
        self.ui.about.clicked.connect(self.aboutClicked)

    def initTherad(self):
        self.threadTimer = ThreadTimer()
        self.threadTimer.timesChange.connect(self.updateTimes)
        self.threadTimer.shiftChange.connect(self.updateShift)
        self.threadTimer.continuousShift.connect(self.updateContinousShift)
        self.threadTimer.start()

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False
        self.shiftHelper = ShiftHelper()

    def loading(self):
        self.loadingCheckAreaFrame()
        self.loadingCheckAreaData()
        self.loadingInteraction()
        self.loadingCheckShiftPage()
        self.loadingAdminView()
        self.loadingCenter()

    def loadingCheckAreaFrame(self):
        shifts = self.SQLHelper.getAllShift()
        rooms = self.SQLHelper.getAllRoom()
        self.ui.loadingCheckAreaFrame(shifts, rooms)

    def loadingCheckAreaData(self):
        now = datetime.now()
        schedules = self.SQLHelper.getScheduleDetailByDate(now.strftime("%Y-%m-%d"))
        crossDaySchedules = self.SQLHelper.getCrossDayScheduleDetailByDate((now-timedelta(days=1)).strftime("%Y-%m-%d"))
        schedules = crossDaySchedules + schedules


        inputDatas = []

        for schedule in schedules:
            inputData = []

            inputData.append(schedule[0])
            inputData.append(f'{schedule[1]:03d}')
            inputData.append(schedule[2])
            inputData.append(schedule[5])
            inputData.append(schedule[7])

            if schedule[8] is None:
                inputData.append("")
            else:
                inputData.append(schedule[8])
            if schedule[9] is None:
                inputData.append("")
            else:
                inputData.append(schedule[9])

            inputData.append(self.shiftHelper.getShiftStatus(schedule[4],schedule[3],schedule[8], schedule[9]))

            inputDatas.append(inputData)

        self.ui.loadingCheckMainList(inputDatas)
        self.ui.loadingCheckShiftData(inputDatas)

    def loadingCheckShiftPage(self):
        now = datetime.now()
        shift = self.shiftHelper.getShiftByTime(now.strftime("%H:%M:%S"))
        self.updateShift(shift[1])

    def loadingInteraction(self):
        self.ui.checkMainNavCheckIn.disconnect()
        self.ui.checkMainNavCheckOut.disconnect()
        self.ui.checkMainNavCheckIn.clicked.connect(self.checkMainNavCheckInClicked)
        self.ui.checkMainNavCheckOut.clicked.connect(self.checkMainNavCheckOutClicked)
        for checkButton in self.ui.checkButtons:
            checkButton.disconnect()
            checkButton.clicked.connect(self.checkButtonClicked)

    def loadingAdminView(self):
        self.ui.funcAreaRight.setHidden(True)

    def loadingCenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()- size.width())/2, (screen.height() - size.height())/2)










    def adminViewClicked(self):
        self.ui.funcAreaRight.setHidden(not self.ui.funcAreaRight.isHidden())

    def windowNavCloseClicked(self):
        self.SQLHelper.close()
        self.threadTimer.stop()

        CloseHandle(globals.mutex)

        app = QApplication.instance()
        app.quit()

    def windowNavMinimizeClicked(self):
        self.showMinimized()

    def windowNavMaximizeClicked(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def importStaffClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = ImportStaffDialog()
            if dialog.exec():
                self.loadingCheckAreaData()
                self.loadingInteraction()

    def importSemesterClicked(self):

        dialog = AuthDialog()
        if dialog.exec():
            dialog = ImportArrangementDialog()
            dialog.setPeriodSelection("學期")
            if dialog.exec():
                self.loadingCheckAreaData()
                self.loadingInteraction()

    def importMidtermClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = ImportArrangementDialog()
            dialog.setPeriodSelection("期中考")
            if dialog.exec():
                self.loadingCheckAreaData()
                self.loadingInteraction()

    def importFinalClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = ImportArrangementDialog()
            dialog.setPeriodSelection("期末考")
            if dialog.exec():
                self.loadingCheckAreaData()
                self.loadingInteraction()

    def importSummberClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = ImportArrangementDialog()
            dialog.setPeriodSelection("暑假")
            if dialog.exec():
                self.loadingCheckAreaData()
                self.loadingInteraction()

    def importWinterClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = ImportArrangementDialog()
            dialog.setPeriodSelection("寒假")
            if dialog.exec():
                self.loadingCheckAreaData()
                self.loadingInteraction()

    def exportIntervalClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = IntervalDialog()
            dialog.comfirm.connect(self.exportIntervalScheduleExcelStart)
            dialog.exec()

    def exportMonthClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            now = datetime.now()
            start = datetime(now.year, now.month, 1)
            end = datetime(now.year, now.month, monthrange(now.year, now.month)[1])

            self.exportIntervalScheduleExcelStart(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

    def exportLastMonthClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            now = datetime.now()
            thisMonthStart = datetime(now.year, now.month, 1)
            lastMonth = thisMonthStart - timedelta(days=1)
            lastMonthStart = datetime(lastMonth.year, lastMonth.month, 1)
            lastMonthEnd = datetime(lastMonth.year, lastMonth.month, monthrange(lastMonth.year, lastMonth.month)[1])

            self.exportIntervalScheduleExcelStart(lastMonthStart.strftime("%Y-%m-%d"),
                                                  lastMonthEnd.strftime("%Y-%m-%d"))
    def editScheduleClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditScheduleDialog()
            dialog.exec()
            self.loadingCheckAreaData()
            self.loadingInteraction()

    def editStaffClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditStaffDialog()
            dialog.exec()
            self.loadingCheckAreaData()
            self.loadingInteraction()

    def editArrangementClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditArrangementDialog()
            dialog.exec()

    def editTodayScheduleClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditTodayScheduleDialog()
            dialog.exec()
            self.loadingCheckAreaData()
            self.loadingInteraction()

    def editShiftClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditShiftDialog()
            dialog.exec()

            self.loadingCheckAreaFrame()
            self.loadingCheckAreaData()
            self.loadingInteraction()
            self.threadTimer.loadingShift()

    def editRoomClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditRoomDialog()
            dialog.exec()

            self.loadingCheckAreaFrame()
            self.loadingCheckAreaData()
            self.loadingInteraction()



    def editVacationClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = EditVacationDialog()
            dialog.exec()

    def changePasswordClicked(self):
        dialog = AuthDialog()
        if dialog.exec():
            dialog = ChgAuthDialog()
            dialog.exec()

    def aboutClicked(self):
        dialog = AboutDialog()
        dialog.exec()

    def switchLeftClicked(self):
        targetIndex = self.ui.checkStacked.currentIndex()+1
        maxIndex = self.ui.checkStacked.count()-1

        if targetIndex > maxIndex:
            targetIndex = 0

        self.ui.checkStacked.setCurrentIndex(targetIndex)

    def switchRightClicked(self):
        targetIndex = self.ui.checkStacked.currentIndex()-1

        if targetIndex<0:
            targetIndex = self.ui.checkStacked.count()-1

        self.ui.checkStacked.setCurrentIndex(targetIndex)

    def checkButtonClicked(self):
        now = datetime.now()
        schedule = self.SQLHelper.getScheduleById(self.sender().property("id"))[0]
        scheduleStatus = self.shiftHelper.getShiftStatus(schedule[3], schedule[2], schedule[5], schedule[6])

        if schedule[5] is None:
            if scheduleStatus in ["未執行","已遲到未執行"]:
                dialog = CheckAuthDialog(schedule[1])
                if dialog.exec():
                    self.SQLHelper.updateScheduleCheckInById(now.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                    self.loadingCheckAreaData()
                    self.loadingInteraction()

                    schedule = self.SQLHelper.getScheduleById(self.sender().property("id"))[0]
                    scheduleStatus = self.shiftHelper.getShiftStatus(schedule[3], schedule[2], schedule[5], schedule[6])
                    dialog = MessageDialog("提示訊息", f"簽到成功，您目前該班的考勤狀態為{scheduleStatus}")
                    dialog.exec()
            else:
                dialog = MessageDialog("錯誤訊息", "簽到時間已過，請聯繫主管人員")
                dialog.exec()
        elif not schedule[5] is None and schedule[6] is None:
            dialog = CheckAuthDialog(schedule[1])
            if dialog.exec():
                self.SQLHelper.updateScheduleCheckOutById(now.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                self.loadingCheckAreaData()
                self.loadingInteraction()

                schedule = self.SQLHelper.getScheduleById(self.sender().property("id"))[0]
                scheduleStatus = self.shiftHelper.getShiftStatus(schedule[3], schedule[2], schedule[5], schedule[6])
                dialog = MessageDialog("提示訊息", f"簽退成功，您目前該班的考勤狀態為{scheduleStatus}")
                dialog.exec()
        elif not schedule[5] is None and not schedule[6] is None:
            dialog = MessageDialog("錯誤訊息", "已簽退，無法重複簽退")
            dialog.exec()

    def checkMainNavCheckInClicked(self):
        now = datetime.now()

        if len(self.ui.checkMainList.selectedItems())!=0:
            schedule = self.SQLHelper.getScheduleById(self.ui.checkMainList.selectedItems()[0].data(0, Qt.UserRole))[0]
            scheduleStatus = self.shiftHelper.getShiftStatus(schedule[3], schedule[2], schedule[5], schedule[6])

            if schedule[5] is None:
                if scheduleStatus in ["未執行", "已遲到未執行"]:
                    dialog = CheckAuthDialog(schedule[1])
                    if dialog.exec():
                        self.SQLHelper.updateScheduleCheckInById(now.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                        self.loadingCheckAreaData()
                        self.loadingInteraction()

                        schedule = self.SQLHelper.getScheduleById(schedule[0])[0]
                        scheduleStatus = self.shiftHelper.getShiftStatus(schedule[3], schedule[2], schedule[5],schedule[6])
                        dialog = MessageDialog("提示訊息", f"簽到成功，您目前該班的考勤狀態為{scheduleStatus}")
                        dialog.exec()

                else:
                    dialog = MessageDialog("錯誤訊息", "簽到時間已過，請聯繫主管人員")
                    dialog.exec()
            else:
                dialog = MessageDialog("錯誤訊息", "已簽到，無法重複簽到")
                dialog.exec()
        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇簽到簽到項目")
            dialog.exec()

    def checkMainNavCheckOutClicked(self):
        now = datetime.now()

        if len(self.ui.checkMainList.selectedItems())!=0:
            schedule = self.SQLHelper.getScheduleById(self.ui.checkMainList.selectedItems()[0].data(0, Qt.UserRole))[0]

            if schedule[5] is None:
                dialog = MessageDialog("錯誤訊息", "無法簽退無簽到記錄之項目")
                dialog.exec()
            elif not schedule[5] is None and schedule[6] is None:
                dialog = CheckAuthDialog(schedule[1])
                if dialog.exec():
                    self.SQLHelper.updateScheduleCheckOutById(now.strftime("%Y-%m-%d %H:%M:%S"), schedule[0])
                    self.loadingCheckAreaData()
                    self.loadingInteraction()

                    schedule = self.SQLHelper.getScheduleById(schedule[0])[0]
                    scheduleStatus = self.shiftHelper.getShiftStatus(schedule[3], schedule[2], schedule[5], schedule[6])
                    dialog = MessageDialog("提示訊息", f"簽退成功，您目前該班的考勤狀態為{scheduleStatus}")
                    dialog.exec()
            elif not schedule[5] is None and not schedule[6] is None:
                dialog = MessageDialog("錯誤訊息", "已簽退，無法重複簽退")
                dialog.exec()
        else:
            dialog = MessageDialog("錯誤訊息", "請先選擇簽到簽退項目")
            dialog.exec()




    def updateTimes(self, date, time, week, shift):
        self.ui.times.setText(f'{date} {time} {week} {shift}')

    def updateShift(self, shiftName):
        for i in range(1, self.ui.checkStacked.count()):
            widget = self.ui.checkStacked.widget(i)
            widgetLayout = widget.layout()

            if widgetLayout.itemAtPosition(0, 0).widget().text() == shiftName:
                self.ui.checkStacked.setCurrentIndex(i)
                break

    def updateContinousShift(self):
        self.loadingCheckAreaData()
        self.loadingInteraction()

    def exportIntervalScheduleExcelStart(self, start, end):

        filePath = QFileDialog.getSaveFileName(self, "匯出檔案", "C:/", "Excel檔案(*.xlsx)")[0]

        if filePath!="":
            self.threadExportIntervalScheduleExcel = ThreadExportIntervalScheduleExcel(start, end, filePath)
            self.threadExportIntervalScheduleExcel.result.connect(self.exportIntervalScheduleExcelEnd)
            self.threadExportIntervalScheduleExcel.start()
            self.dialog = NoncancelableDialog("提示訊息", "正在匯出資料，請稍候")
            self.dialog.exec()

    def exportIntervalScheduleExcelEnd(self, result, filePath):
        self.dialog.hide()
        del self.dialog

        if result==0:
            dialog = MessageDialog("提示訊息", "匯出資料成功，按下確認後開啟Excel檔案")
            if dialog.exec():
                os.system(f'start {filePath}')
        elif result==1:
            dialog = MessageDialog("錯誤訊息", "匯出資料失敗，請聯絡程式開發人員")
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


class ThreadExportIntervalScheduleExcel(QThread):

    result = pyqtSignal(int, str)

    def __init__(self, startTime, endTime, filePath):
        super(ThreadExportIntervalScheduleExcel, self).__init__()
        self.init(startTime, endTime, filePath)

    def init(self, startTime, endTime, filePath):
        self.initSQL()
        self.initOther()
        self.initValue(startTime, endTime, filePath)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.ShiftHelper = ShiftHelper()

    def initValue(self, startTime, endTime, filePath):
        self.startTime = startTime
        self.endTime = endTime
        self.filePath = filePath

    def run(self):
        data = self.dataPrepare()

        self.generateExcel(data[0], data[1])

        self.result.emit(0, self.filePath)

    def dataPrepare(self):
        statisticsDict = {}
        for staff in self.SQLHelper.getAllStaff():
            statisticsDict[staff[0]] = {"staffNum": staff[0], "staffName": staff[2], "stuNum": staff[1], "ontime": 0,
                                        "late": 0, "excused": 0, "lateWithExcused": 0, "absent": 0, "noCheckOut": 0,
                                        "executing": 0, "unexecuted": 0}

        schedules = self.SQLHelper.getScheduleDetailWithShiftByDateInterval(self.startTime, self.endTime)

        records = []
        statistics = []

        for schedule in schedules:
            scheduleStatus = self.ShiftHelper.getShiftStatus(schedule[4], schedule[1], schedule[12], schedule[13])

            records.append(
                [schedule[1], schedule[5], schedule[11], schedule[2], schedule[3], schedule[12], schedule[13], scheduleStatus])

            print(schedule)

            if scheduleStatus in ["準時"]:
                statisticsDict[schedule[2]]["ontime"] += schedule[9]
            elif scheduleStatus in ["遲到"]:
                statisticsDict[schedule[2]]["late"] += schedule[9]
            elif scheduleStatus in ["早退"]:
                statisticsDict[schedule[2]]["excused"] += schedule[9]
            elif scheduleStatus in ["遲到早退"]:
                statisticsDict[schedule[2]]["lateWithExcused"] += schedule[9]
            elif scheduleStatus in ["未簽退"]:
                statisticsDict[schedule[2]]["noCheckOut"] += schedule[9]
            elif scheduleStatus in ["執行中", "已遲到執行中"]:
                statisticsDict[schedule[2]]["executing"] += schedule[9]
            elif scheduleStatus in ["未執行", "已遲到未執行"]:
                statisticsDict[schedule[2]]["unexecuted"] += schedule[9]
            elif scheduleStatus in ["曠班"]:
                statisticsDict[schedule[2]]["absent"] += schedule[9]

        for statistic in sorted(statisticsDict.items(), key=lambda statistic: statistic[0]):
            statistics.append(
                [statistic[1]["staffNum"], statistic[1]["staffName"], statistic[1]["stuNum"], statistic[1]["ontime"],
                 statistic[1]["late"], statistic[1]["excused"], statistic[1]["lateWithExcused"], statistic[1]["absent"],
                 statistic[1]["noCheckOut"], statistic[1]["executing"], statistic[1]["unexecuted"]])

        return statistics, records


    def generateExcel(self, statistics, records):
        app = xw.App(visible=False, add_book=False)
        wb = app.books.add()
        wb.sheets[0].name = "統計資料表"

        # 資料寫入
        shtStatistics = wb.sheets["統計資料表"]
        shtStatistics.range('A1:K2').api.merge()
        shtStatistics.range('A1').value = f'{self.startTime} 至 {self.endTime} 淡江大學資訊處考勤統計資料表'
        shtStatistics.range('A3').value = ["工讀生編號", "工讀生姓名", "工讀生學號", "準時", "遲到", "早退", "遲到早退", "曠班", "未簽退", "執行中","未執行"]
        shtStatistics.range('A4').value = statistics

        # 樣式寫入
        shtStatistics.range('A:K').api.Font.Name = "微軟正黑體"
        shtStatistics.range('A:K').api.Font.Size = 12
        shtStatistics.range('A:K').api.HorizontalAlignment = -4108
        shtStatistics.range('A:K').api.VerticalAlignment = -4108
        shtStatistics.range('A:K').api.EntireColumn.AutoFit()
        shtStatistics.range('A1').api.Font.Size = 14
        shtStatistics.range('A1').api.Font.Bold = True

        wb.sheets.add("打卡紀錄表", after=shtStatistics)
        shtRecord = wb.sheets["打卡紀錄表"]

        # 資料寫入
        shtRecord.range('A1:H2').api.merge()
        shtRecord.range('A1').value = f'{self.startTime} 至 {self.endTime} 淡江大學資訊處考勤打卡紀錄表'
        shtRecord.range('A3').value = ["日期", "班別", "實習室", "工讀生編號", "工讀生姓名", "簽到時間", "簽退時間", "簽到狀況"]
        shtRecord.range('A4').value = records

        # 樣式寫入
        shtRecord.range('A:H').api.Font.Name = "微軟正黑體"
        shtRecord.range('A:H').api.Font.Size = 12
        shtRecord.range('A:H').api.HorizontalAlignment = -4108
        shtRecord.range('A:H').api.VerticalAlignment = -4108
        shtRecord.range('A:H').api.EntireColumn.AutoFit()
        shtRecord.range('A1').api.Font.Size = 14
        shtRecord.range('A1').api.Font.Bold = True

        wb.save(self.filePath)
        wb.close()
        app.quit()


class ThreadTimer(QThread):

    timesChange = pyqtSignal(str, str, str, str)
    shiftChange = pyqtSignal(str)
    continuousShift = pyqtSignal()
    runFlag = True
    autoCheckList = []


    def __init__(self):
        super(ThreadTimer, self).__init__()
        self.init()

    def init(self):
        self.initSQL()
        self.initOther()
        self.initValue()

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.ShiftHelper = ShiftHelper()

    def initValue(self):
        self.shifts = self.SQLHelper.getAllShift()

    def loadingShift(self):
        self.shifts = self.SQLHelper.getAllShift()

    def run(self):
        while self.runFlag:
            now = datetime.now()
            lastShift, currentShift, nextShift = self.distrituteShift(now.strftime("%H:%M:%S"))

            self.updateTimes(now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), now.weekday(), currentShift[1])
            self.checkShiftChange(now.strftime("%H:%M:%S"), currentShift, nextShift)
            self.checkContinuousShift(now.strftime("%Y-%m-%d %H:%M:%S"), lastShift, currentShift, nextShift)

            self.sleep(1)


    def distrituteShift(self, time):
        time = datetime.strptime(time, "%H:%M:%S")

        lastShift = None
        currentShift = None
        nextShift = None

        for i in range(0, len(self.shifts)):
            start = datetime.strptime(f'{self.shifts[i][2]}', "%H:%M:%S")
            end = datetime.strptime(f'{self.shifts[i][3]}', "%H:%M:%S")
            if start>end:
                end += timedelta(days=1)

            if start <= time <= end:
                currentShift = self.shifts[i]

                if i==len(self.shifts)-1:
                    nextShift = self.shifts[0]
                else:
                    nextShift = self.shifts[i+1]

                if i==0:
                    lastShift = self.shifts[-1]
                else:
                    lastShift = self.shifts[i-1]

                break

        return lastShift, currentShift, nextShift

    def updateTimes(self, date, time, week, shift):
        weekTrans = {0:"星期一", 1:"星期二", 2:"星期三", 3:"星期四", 4:"星期五", 5:"星期六", 6: "星期日"}
        self.timesChange.emit(date, time, weekTrans[week], shift)

    def checkShiftChange(self, time, currentShift, nextShift):
        time = datetime.strptime(time, "%H:%M:%S")
        currentShiftEndTime = datetime.strptime(f'{currentShift[3]}', "%H:%M:%S")

        if time == currentShiftEndTime:
            self.shiftChange.emit(nextShift[1])

    def checkContinuousShift(self, now, lastShift, currentShift, nextShift):

        now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        time = datetime.strptime(now.strftime("%H:%M:%S"), "%H:%M:%S")
        currentShiftEndTime = datetime.strptime(f'{currentShift[3]}', "%H:%M:%S")
        nextShiftStartTime = datetime.strptime(f'{nextShift[2]}', "%H:%M:%S")

        # 29秒時執行
        if time == nextShiftStartTime - timedelta(seconds=1):

            currentShiftSchedules = self.SQLHelper.getScheduleYesCheckInNoCheckOutByDateAndShift(
                now.strftime("%Y-%m-%d"), currentShift[0])
            nextShiftSchedules = self.SQLHelper.getScheduleNoCheckInByDateAndShift(now.strftime("%Y-%m-%d"),
                                                                                   nextShift[0])

            currentShiftStaffMap = {}
            for schedule in currentShiftSchedules:
                if schedule[1] not in currentShiftStaffMap:
                    currentShiftStaffMap[schedule[1]] = []
                currentShiftStaffMap[schedule[1]].append(schedule[0])

            self.autoCheckList.clear()
            autoCheckIns = []
            for schedule in nextShiftSchedules:
                if schedule[1] in currentShiftStaffMap:
                    autoCheckIns.append(schedule[0])
                    self.autoCheckList.append(schedule[1])

            nextShiftShouldCheckIn = datetime.strptime(f'{now.strftime("%Y-%m-%d")} {nextShift[2]}', "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)


            for autoCheckIn in autoCheckIns:
                self.SQLHelper.updateScheduleCheckInById(nextShiftShouldCheckIn, autoCheckIn)


            self.continuousShift.emit()

        # 30秒時執行
        if time == currentShiftEndTime:

            currentShiftSchedules = self.SQLHelper.getScheduleYesCheckInNoCheckOutByDateAndShift(now.strftime("%Y-%m-%d"), currentShift[0])

            currentShiftStaffMap = {}
            for schedule in currentShiftSchedules:
                if schedule[1] not in currentShiftStaffMap:
                    currentShiftStaffMap[schedule[1]] = []
                currentShiftStaffMap[schedule[1]].append(schedule[0])

            autoCheckOuts = []

            for autoCheck in self.autoCheckList:
                if autoCheck in currentShiftStaffMap:
                    for item in currentShiftStaffMap[autoCheck]:
                        autoCheckOuts.append(item)

            currentShiftShouldCheckIn = datetime.strptime(f'{now.strftime("%Y-%m-%d")} {currentShift[2]}',
                                                          "%Y-%m-%d %H:%M:%S")
            currentShiftShouldCheckOut = datetime.strptime(f'{now.strftime("%Y-%m-%d")} {currentShift[3]}',
                                                           "%Y-%m-%d %H:%M:%S")
            if currentShiftShouldCheckOut < currentShiftShouldCheckIn:
                currentShiftShouldCheckOut += timedelta(days=1)

            for autoCheckOut in autoCheckOuts:
                self.SQLHelper.updateScheduleCheckOutById(currentShiftShouldCheckOut.strftime("%Y-%m-%d %H:%M:%S"), autoCheckOut)

            self.autoCheckList.clear()

            self.continuousShift.emit()












    def stop(self):
        self.runFlag = False

