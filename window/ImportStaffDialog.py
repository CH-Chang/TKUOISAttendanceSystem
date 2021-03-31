import os
import pandas

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.Ui_ImportStaffDialog import Ui_ImortStaffDialog
from utils.SQLHelper import SQLHelper

class ImportStaffDialog(QDialog):

    list = []

    def __init__(self):
        super(ImportStaffDialog, self).__init__()
        self.init()

    def init(self):
        self.initUI()
        self.initInteraction()
        self.initSQL()
        self.initOther()

    def initUI(self):
        self.ui = Ui_ImortStaffDialog()
        self.ui.setupUi(self)

    def initInteraction(self):
        self.ui.dialogNavClose.clicked.connect(self.dialogNavCloseClicked)
        self.ui.cancel.clicked.connect(self.cancelCliecked)
        self.ui.pickFile.clicked.connect(self.pickFileClicked)
        self.ui.comfirm.clicked.connect(self.comfirmClicked)

    def initSQL(self):
        self.SQLHelper = SQLHelper()

    def initOther(self):
        self.moveFlag = False



    def pickFileClicked(self):
        fileUrls = QFileDialog.getOpenFileUrl(self, "選取工讀生資料", QUrl(os.getcwd()), "Excel檔案 (*.xlsx)")
        fileUrl = fileUrls[0].toLocalFile()

        if fileUrl!="":
            excel = pandas.read_excel(fileUrl, sheet_name=0, header=None, converters={0: str, 1: str, 2: str})
            self.list = excel.values.tolist()

            self.ui.loadingList(self.list)

    def comfirmClicked(self):
        self.SQLHelper.delAllStaff()
        self.SQLHelper.newAllStaff(self.list)
        self.SQLHelper.close()
        self.accept()

    def dialogNavCloseClicked(self):
        self.SQLHelper.close()
        self.reject()

    def cancelCliecked(self):
        self.SQLHelper.close()
        self.reject()

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

