from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

from ui.Ui_EditShiftCellDialog import Ui_EditShiftCellDialog

from window.MessageDialog import MessageDialog

from utils.SQLHelper import SQLHelper

class EditShiftCellDialog(QDialog):

    def __init__(self, shiftId):
        super(EditShiftCellDialog, self).__init__()
        self.init(shiftId)
        self.loading()


    def init(self, shiftId):
        self.initUI()
        self.initSQL()
        self.initOther()
        self.initInteraction()
        self.initValue(shiftId)

    def initUI(self):
        self.ui = Ui_EditShiftCellDialog()
        self.ui.setupUi(self)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False

    def initValue(self, shiftId):
        self.shiftId = shiftId


    def initInteraction(self):
        self.ui.cancel.clicked.connect(self.cancelClicked)
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)
        self.ui.nameLineEdit.returnPressed.connect(self.nameLineEditReturnPressed)
        self.ui.hourLineEdit.returnPressed.connect(self.hourLineEditReturnPressed)
        self.ui.payHourLineEdit.returnPressed.connect(self.payHourLineEditReturnPressed)

    def loading(self):
        self.loadingData()
        self.loadingData()

    def loadingData(self):
        now = datetime.now()

        if not self.shiftId is None:
            shift = self.SQLHelper.getShiftById(self.shiftId)[0]

            shiftStartTime = datetime.strptime(shift[2], "%H:%M:%S")
            shiftEndTime = datetime.strptime(shift[3], "%H:%M:%S")

            self.ui.nameLineEdit.setText(shift[1])
            self.ui.hourLineEdit.setText(str(shift[4]))
            self.ui.timeStart.setTime(QTime(shiftStartTime.hour, shiftStartTime.minute, shiftStartTime.second))
            self.ui.timeEnd.setTime(QTime(shiftEndTime.hour, shiftEndTime.minute, shiftEndTime.second))
            self.ui.payHourLineEdit.setText(str(shift[5]))
        else:
            self.ui.timeStart.setTime(QTime(now.hour, now.minute, now.second))
            self.ui.timeEnd.setTime(QTime(now.hour, now.minute, now.second))

    def loadingFocus(self):
        self.ui.nameLineEdit.setFocus(True)



    def cancelClicked(self):
        self.SQLHelper.close()
        self.reject()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def comfirmClicked(self):
        startTime = self.ui.timeStart.time()
        endTime = self.ui.timeEnd.time()

        name = self.ui.nameLineEdit.text()
        start = f'{startTime.hour():02d}:{startTime.minute():02d}:{startTime.second():02d}'
        end = f'{endTime.hour():02d}:{endTime.minute():02d}:{endTime.second():02d}'
        hour = self.ui.hourLineEdit.text()
        payHour = self.ui.payHourLineEdit.text()

        if name=='' or hour=='' or payHour=='':
            dialog = MessageDialog("錯誤訊息", "請確認表單內容填寫完整")
            dialog.exec()
        else:
            if self.shiftId is None:
                dialog = MessageDialog("提示訊息", "請確認是否新增該筆班別資料")
                if dialog.exec():
                    self.SQLHelper.newShift(name, start, end, float(hour), float(payHour))
                    self.accept()

            else:
                dialog = MessageDialog("提示訊息", "請確認是否修改該筆班別資料")
                if dialog.exec():
                    self.SQLHelper.updateShiftById(self.shiftId, name, start, end, float(hour), float(payHour))
                    self.accept()

    def nameLineEditReturnPressed(self):
        self.ui.timeStart.setFocus(True)

    def hourLineEditReturnPressed(self):
        self.ui.payHourLineEdit.setFocus(True)

    def payHourLineEditReturnPressed(self):
        self.comfirmClicked()
















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