from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

from ui.Ui_EditVacationCellDialog import Ui_EditVacationCellDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper

class EditVacationCellDialog(QDialog):

    def __init__(self, periodId):
        super(EditVacationCellDialog, self).__init__()
        self.init(periodId)
        self.loading()


    def init(self, periodId):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()
        self.initValue(periodId)

    def initUI(self):
        self.ui = Ui_EditVacationCellDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initValue(self, periodId):
        self.periodId = periodId


    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)

    def loading(self):
        if not self.periodId is None:
            period = self.SQLHelper.getPeriodById(self.periodId)[0]
            periodStartDate = datetime.strptime(period[2], "%Y-%m-%d")
            periodEndDate = datetime.strptime(period[3], "%Y-%m-%d")

            self.ui.nameLineEdit.setText(period[1])
            self.ui.dateStart.setDate(QDate(periodStartDate.year, periodStartDate.month, periodStartDate.day))
            self.ui.dateEnd.setDate(QDate(periodEndDate.year, periodEndDate.month, periodEndDate.day))

    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):

        startDate = self.ui.dateStart.date()
        endDate = self.ui.dateEnd.date()

        name = self.ui.nameLineEdit.text().strip()
        start = f'{startDate.year():04d}-{startDate.month():02d}-{startDate.day():02d}'
        end = f'{endDate.year():04d}-{endDate.month():02d}-{endDate.day():02d}'

        if name=='':
            dialog = MessageDialog("錯誤訊息", "請確認表單內容填寫完整")
            dialog.exec()
        else:
            if self.periodId is None:
                dialog = MessageDialog("提示訊息", "請確認是否新增該筆假日項目")
                if dialog.exec():
                    self.SQLHelper.newPeriodVacation(name, start, end)
                    self.accept()
            else:
                dialog = MessageDialog("提示訊息", "請確認是否修改該筆假日項目")
                if dialog.exec():
                    self.SQLHelper.updatePeriodById(self.periodId, name, start, end)
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