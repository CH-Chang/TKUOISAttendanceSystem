# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\桌面\TKUIofoCenterClient\uiFile\EditArrangementDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.SvgHelper import SvgHelper

from icon.svg import close, logoIcon


class Ui_EditArrangementDialog(object):
    def setupUi(self, EditArrangementDialog):
        EditArrangementDialog.setObjectName("EditArrangementDialog")
        EditArrangementDialog.setWindowFlags(Qt.CustomizeWindowHint)
        EditArrangementDialog.resize(1000, 450)
        EditArrangementDialog.setAutoFillBackground(False)
        EditArrangementDialog.setStyleSheet("QDialog{background-color:white;}")

        self.retranslateUi(EditArrangementDialog)
        QMetaObject.connectSlotsByName(EditArrangementDialog)

        self.setupMainLayout(EditArrangementDialog)
        self.setupDialogNav()
        self.setupCenterialArea()
        self.setupContentArea()
        self.setupNavArea()

    def retranslateUi(self, EditArrangementDialog):
        _translate = QCoreApplication.translate
        EditArrangementDialog.setWindowTitle(_translate("EditArrangementDialog", "班表編輯"))
        EditArrangementDialog.setWindowIcon(QIcon(SvgHelper.getQPixmapFromBytes(logoIcon, QSize(512, 512))))


    def setupMainLayout(self, EditArrangementDialog):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        EditArrangementDialog.setLayout(self.mainLayout)

    def setupDialogNav(self):
        dialogNav = QWidget()
        dialogNavLayout = QHBoxLayout()

        self.dialogNavClose = QPushButton()
        self.dialogNavClose.setIcon(QIcon(SvgHelper.getQPixmapFromBytes(close, QSize(12, 12))))
        self.dialogNavClose.setIconSize(QSize(12, 12))
        self.dialogNavClose.resize(12, 12)
        self.dialogNavClose.setStyleSheet(
            "QPushButton{background-color: transparent; border-style:none; padding: 3px 3px 3px 3px;} QPushButton:hover{background-color: #eeeeee; border-style:none; border-radius:5px; padding: 3px 3px 3px 3px;} QPushButton:pressed{background-color: #999999; border-style:none; border-radius:5px; padding: 3px 3px 3px 3px;}")
        self.dialogNavClose.setCursor(QCursor(Qt.PointingHandCursor))

        dialogNavLayout.addStretch()
        dialogNavLayout.addWidget(self.dialogNavClose)

        dialogNav.setLayout(dialogNavLayout)

        self.mainLayout.addWidget(dialogNav, alignment=Qt.AlignTop)

    def setupCenterialArea(self):
        centerialArea = QWidget()
        self.centerialAreaLayout = QHBoxLayout()
        centerialArea.setLayout(self.centerialAreaLayout)

        self.mainLayout.addWidget(centerialArea)

    def setupContentArea(self):
        contentArea = QWidget()
        contentAreaLayout = QVBoxLayout()

        self.listArea = QTreeWidget()
        self.listArea.setFont(QFont("Noto Sans TC Regular", 10))
        self.listArea.setStyleSheet(
            "QHeaderView::section{color: #f7931e; border: 0; background-color: white;} QTreeWidget{border-style: none;} QTreeWidget::item:hover{background-color: #FFD4A2; color: black;} QTreeWidget::item:selected{background-color: #FCA642; color: white;}")
        self.listArea.setHeaderLabels(["星期", "工讀生編號", "工讀生姓名", "班別", "實習室", "時期"])
        self.listArea.header().setDefaultAlignment(Qt.AlignCenter)
        self.listArea.horizontalScrollBar().setStyleSheet(
            "QScrollBar:horizontal{ border-radius: 5px; background: white; padding-left:2px; padding-right: 2px;} QScrollBar::handle:horizontal{background: #9F9F9F; border-radius: 5px; margin-top: 3px; margin-bottom: 3px;} QScrollBar::handle:horizontal:hover{background: #3d3d3d; border-radius: 5px; margin-top: 3px; margin-bottom: 3px;} QScrollBar::add-line:horizontal{height: 0px; width: 0px; image: url('')} QScrollBar::sub-line:horizontal{height: 0px; width: 0px; image: url('')}")
        self.listArea.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical{ border-radius: 5px; background: white; padding-top:2px; padding-bottom: 2px;} QScrollBar::handle:vertical{background: #9F9F9F; border-radius: 5px; margin-left: 3px; margin-right: 3px;} QScrollBar::handle:vertical:hover{background: #3d3d3d; border-radius: 5px; margin-left: 3px; margin-right: 3px;} QScrollBar::add-line:horizontal{height: 0px; width: 0px; image: url('')} QScrollBar::sub-line:vertical{height: 0px; width: 0px; image: url('')}")

        contentAreaLayout.addWidget(self.listArea)
        contentArea.setLayout(contentAreaLayout)

        self.centerialAreaLayout.addWidget(contentArea)

    def setupNavArea(self):
        navArea = QWidget()
        navAreaLayout = QVBoxLayout()


        self.delete = QPushButton()
        self.delete.setText("刪除項目")
        self.delete.setFont(QFont("Noto Sans TC Regular", 10))
        self.delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete.setStyleSheet(
            "QPushButton{color:#f7931e; border-style: none; border: 1px solid #f7931e; border-radius: 5px; padding: 5px 8px 5px 8px; background-color: white;} QPushButton:hover{color: white; background-color:#f7931e} QPushButton:pressed{color: white; background-color:#DC831A}")

        self.add = QPushButton()
        self.add.setText("新增項目")
        self.add.setFont(QFont("Noto Sans TC Regular", 10))
        self.add.setCursor(QCursor(Qt.PointingHandCursor))
        self.add.setStyleSheet(
            "QPushButton{color:#f7931e; border-style: none; border: 1px solid #f7931e; border-radius: 5px; padding: 5px 8px 5px 8px; background-color: white;} QPushButton:hover{color: white; background-color:#f7931e} QPushButton:pressed{color: white; background-color:#DC831A}")

        self.edit = QPushButton()
        self.edit.setText("修改項目")
        self.edit.setFont(QFont("Noto Sans TC Regular", 10))
        self.edit.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit.setStyleSheet(
            "QPushButton{color:#f7931e; border-style: none; border: 1px solid #f7931e; border-radius: 5px; padding: 5px 8px 5px 8px; background-color: white;} QPushButton:hover{color: white; background-color:#f7931e} QPushButton:pressed{color: white; background-color:#DC831A}")

        self.cancel = QPushButton()
        self.cancel.setText("關閉視窗")
        self.cancel.setFont(QFont("Noto Sans TC Regular", 10))
        self.cancel.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel.setStyleSheet(
            "QPushButton{color:#f7931e; border-style: none; border: 1px solid #f7931e; border-radius: 5px; padding: 5px 8px 5px 8px; background-color: white;} QPushButton:hover{color: white; background-color:#f7931e} QPushButton:pressed{color: white; background-color:#DC831A}")


        navAreaLayout.addWidget(self.add)
        navAreaLayout.addWidget(self.delete)
        navAreaLayout.addWidget(self.edit)
        navAreaLayout.addWidget(self.cancel)
        navAreaLayout.addStretch()
        navArea.setLayout(navAreaLayout)

        self.centerialAreaLayout.addWidget(navArea, alignment=Qt.AlignRight)


    def loadingList(self, data: list):
        self.listArea.clear()

        for item in data:
            qTreeWidgetItem = QTreeWidgetItem(item[1:])
            qTreeWidgetItem.setData(0, Qt.UserRole, item[0])
            for i in range(0, qTreeWidgetItem.columnCount()):
                qTreeWidgetItem.setTextAlignment(i, Qt.AlignCenter)

            self.listArea.addTopLevelItem(qTreeWidgetItem)


