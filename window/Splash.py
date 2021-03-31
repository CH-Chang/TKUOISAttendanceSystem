import os, subprocess

import globals

from datetime import datetime, timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from utils.FontHelper import FontHelper
from utils.SQLHelper import SQLHelper
from ui.Ui_Splash import Ui_Splash
from window.MainWindow import MainWindow

class Splash(QWidget):

    def __init__(self):
        super(Splash, self).__init__()
        self.initUI()
        self.initThread()
        self.initInteraction()
        self.initOther()
        self.init()
        self.loading()


    def initUI(self):
        self.ui = Ui_Splash()
        self.ui.setupUi(self)

    def initThread(self):
        self.initProgram = ThreadInitProgram()
        self.initFont = ThreadInitFont()
        self.initDB = ThreadInitDB()
        self.checkNetWork = ThreadCheckNetwork()

    def initInteraction(self):
        self.initProgram.started.connect(self.initProgramStarted)
        self.initProgram.result.connect(self.initProgramFinished)
        self.initFont.started.connect(self.initFontStarted)
        self.initFont.result.connect(self.initFontFinished)
        self.initDB.started.connect(self.initDBStarted)
        self.initDB.result.connect(self.initDBFinished)
        self.checkNetWork.started.connect(self.checkNetworkStarted)
        self.checkNetWork.result.connect(self.checkNetworkFinished)

    def initOther(self):
        self.moveFlag = False

    def init(self):
        self.initProgram.start()


    def initProgramStarted(self):
        self.ui.status.setText("正在初始化系統 請稍候")

    def initProgramFinished(self, res):
        if res==0:
            self.ui.status.setText("系統初始化成功")
            self.initFont.start()
        else:
            app = QApplication.instance()
            app.quit()

    def initFontStarted(self):
        self.ui.status.setText("正在初始化字型文件 請稍候")

    def initFontFinished(self, res):
        if res==0:
            self.ui.status.setText("字型文件初始化成功")
            self.initDB.start()
        else:
            app = QApplication.instance()
            app.quit()

    def initDBStarted(self):
        self.ui.status.setText("正在初始化資料庫 請稍候")

    def initDBFinished(self, res):
        if res==0:
            self.ui.status.setText("資料庫初始化成功")
            self.checkNetWork.start()
        else:
            app = QApplication.instance()
            app.quit()

    def loading(self):
        self.loadingCenter()

    def loadingCenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def checkNetworkStarted(self):
        self.ui.status.setText("正在檢測網路環境")

    def checkNetworkFinished(self, res):
        if res==0:
            self.ui.status.setText("連結網路成功，請等候跳轉")
            self.enterSystem()
        elif res==1:
            self.ui.status.setText("目前無法連結網路，請等候跳轉")
            self.enterSystem()

    def enterSystem(self):
        globals.window.hide()
        globals.window = MainWindow()
        globals.window.show()

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

class ThreadInitProgram(QThread):

    result = pyqtSignal(int)

    def __init__(self):
        super(ThreadInitProgram, self).__init__()

    def run(self):
        path = os.getcwd()
        if not os.path.isdir(path+"\\db"):
            os.mkdir(path+"\\db")
        self.result.emit(0)

class ThreadInitFont(QThread):

    result = pyqtSignal(int)

    def __init__(self):
        super(ThreadInitFont, self).__init__()

    def run(self):
        FontHelper.initNotoSansTCRegular()
        self.result.emit(0)





class ThreadInitDB(QThread):

    result = pyqtSignal(int)

    def __init__(self):
        super(ThreadInitDB, self).__init__()

    def run(self):
        self.SQLHelper = SQLHelper()
        if not self.SQLHelper.isDBFailed():
            self.syncSchedule()
            self.SQLHelper.close()
            self.result.emit(0)
        else:
            self.result.emit(1)

    def syncSchedule(self):
        try:
            lastSyncedDate = datetime.strptime(self.SQLHelper.getSyncSchedule(), "%Y-%m-%d")
        except:
            lastSyncedDate = None

        now = datetime.now()

        if lastSyncedDate is None:
            period = self.SQLHelper.getPeriodByDate(now.strftime("%Y-%m-%d"))
            if len(period)!=0:
                periodId = period[0][0]
                weekday = now.weekday()
                arrangements = self.SQLHelper.getArrangementByPeriodAndWeek(periodId, weekday)
                self.SQLHelper.newSchedules(now.strftime("%Y-%m-%d"), arrangements)

            self.SQLHelper.updateSyncSchedule(now.strftime("%Y-%m-%d"))
        else:
            while lastSyncedDate.date()!=now.date():
                lastSyncedDate+=timedelta(days=1)

                period = self.SQLHelper.getPeriodByDate(lastSyncedDate.strftime("%Y-%m-%d"))
                if len(period)!=0:
                    periodId = period[0][0]
                    weekday = now.weekday()
                    arrangements = self.SQLHelper.getArrangementByPeriodAndWeek(periodId, weekday)
                    self.SQLHelper.newSchedules(lastSyncedDate.strftime("%Y-%m-%d"), arrangements)

                self.SQLHelper.updateSyncSchedule(lastSyncedDate.strftime("%Y-%m-%d"))











class ThreadCheckNetwork(QThread):

    result = pyqtSignal(int)

    def __init__(self):
        super(ThreadCheckNetwork, self).__init__()

    def run(self):
        connected = subprocess.call(['ping', '-n', '1', 'www.google.com'])
        if connected ==0:
            self.result.emit(0)
        else:
            self.result.emit(1)
