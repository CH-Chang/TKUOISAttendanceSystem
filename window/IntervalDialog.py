from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime

from ui.Ui_IntervalDialog import Ui_IntervalDialog

class IntervalDialog(QDialog):

    comfirm = pyqtSignal(str, str)

    def __init__(self):
        super(IntervalDialog, self).__init__()
        self.init()
        self.loading()

    def init(self):
        self.initUI()
        self.initInteraction()

    def initUI(self):
        self.ui = Ui_IntervalDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)

    def initOther(self):
        self.moveFlag = False

    def loading(self):
        self.loadingDate()
        self.loadingFocus()

    def loadingDate(self):
        now = datetime.now()

        self.ui.interavalStart.setDate(QDate(now.year, now.month, now.day))
        self.ui.interavalEnd.setDate(QDate(now.year, now.month, now.day))

    def loadingFocus(self):
        self.ui.interavalStart.setFocus(True)

    def dialogNavCloseClicked(self):
        self.reject()

    def cancelClicked(self):
        self.reject()

    def comfirmClicked(self):
        startDate = self.ui.interavalStart.date()
        endDate = self.ui.interavalEnd.date()
        start = f'{startDate.year():04d}-{startDate.month():02d}-{startDate.day():02d}'
        end = f'{endDate.year():04d}-{endDate.month():02d}-{endDate.day():02d}'

        self.comfirm.emit(start, end)
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