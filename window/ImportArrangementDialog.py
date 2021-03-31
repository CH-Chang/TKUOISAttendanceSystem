import pandas
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

from ui.Ui_ImportArrangementDialog import Ui_ImportArrangementDialog
from utils.SQLHelper import SQLHelper

from window.MessageDialog import MessageDialog


class ImportArrangementDialog(QDialog):

    list = []

    def __init__(self):
        super(ImportArrangementDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initInteraction()
        self.initSQL()
        self.initOther()

    def initUI(self):
        self.ui = Ui_ImportArrangementDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.pickFile.clicked.connect(self.pickFileClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)

        self.ui.periodSelection.currentTextChanged.connect(self.periodSelectionChanged)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def loading(self):
        self.loadingPeriod()
        self.loadingDate()

    def loadingPeriod(self):
        periods = self.SQLHelper.getPeriodNotVacation()
        data = []
        for period in periods:
            data.append(period[1])
        self.ui.loadingPeriodSelection(data)

    def loadingDate(self):
        periodName = self.ui.periodSelection.currentText()
        period = self.SQLHelper.getPeriodByName(periodName)

        startDate = datetime.strptime(period[0][2],"%Y-%m-%d")
        start = QDate(startDate.year, startDate.month, startDate.day)

        endDate = datetime.strptime(period[0][3], "%Y-%m-%d")
        end = QDate(endDate.year, endDate.month, endDate.day)

        self.ui.loadingPeriodDate(start, end)




    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def pickFileClicked(self):
        fileUrls = QFileDialog.getOpenFileUrl(self, "選取工讀生資料", QUrl(os.getcwd()), "Excel檔案 (*.xlsx)")
        fileUrl = fileUrls[0].toLocalFile()

        if fileUrl != "":
            excel = pandas.read_excel(fileUrl, sheet_name=0, header=None, converters={0: str, 1: str, 2: str, 3: str})
            self.list = excel.values.tolist()

            self.ui.loadingList(self.list)

    def comfirmClicked(self):
        period = self.SQLHelper.getPeriodByName(self.ui.periodSelection.currentText())[0]

        start = self.ui.dateStart.date()
        end = self.ui.dateEnd.date()
        self.SQLHelper.updatePeriodStartAndEndById(f"{start.year():04d}-{start.month():02d}-{start.day():02d}", f"{end.year():04d}-{end.month():02d}-{end.day():02d}", period[0])

        data = []
        weekTrans = { "星期一":0, "星期二":1, "星期三":2, "星期四":3, "星期五":4, "星期六":5, "星期日":6}
        for item in self.list:
            room = self.SQLHelper.getRoomByName(item[4])
            shift = self.SQLHelper.getShiftByName(item[3])
            data.append([int(item[0]), weekTrans[item[2]], shift[0][0], room[0][0], period[0]])
        self.SQLHelper.delArrangementByPeriod(period[0])
        self.SQLHelper.newArrangements(data)

        self.reloadTodaySchedules(period)

        self.SQLHelper.close()
        self.accept()


    def periodSelectionChanged(self, text):
        self.loadingDate()


    def setPeriodSelection(self, period: str):
        self.ui.periodSelection.setCurrentText(period)


    def reloadTodaySchedules(self, updatePeriod):

        now = datetime.now()
        todayPeriod = self.SQLHelper.getPeriodByDate(now.strftime("%Y-%m-%d"))

        if len(todayPeriod)!=0:
            todayPeriod = todayPeriod[0]

            if todayPeriod[0]==updatePeriod[0]:
                dialog = MessageDialog("提示訊息", "請問是否重新載入今日所有已執行及未執行之班表")
                if dialog.exec():
                    self.SQLHelper.delScheduleByDate(now.strftime("%Y-%m-%d"))
                    arrangements = self.SQLHelper.getArrangementByPeriodAndWeek(todayPeriod[0], now.weekday())
                    self.SQLHelper.newSchedules(now.strftime("%Y-%m-%d"), arrangements)





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
