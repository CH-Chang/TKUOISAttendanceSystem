# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\桌面\TKUIofoCenterClient\uiFile\Splash.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *


from icon.svg import logoWhite, logoIcon
from utils.SvgHelper import SvgHelper


class Ui_Splash(object):
    def setupUi(self, Splash):
        Splash.setObjectName("Splash")
        Splash.resize(600, 400)
        Splash.setFixedSize(600, 400)
        Splash.setAutoFillBackground(True)
        Splash.setStyleSheet("QWidget{background-color: #F7931E;}")
        Splash.setWindowFlags(Qt.FramelessWindowHint)

        self.retranslateUi(Splash)
        QMetaObject.connectSlotsByName(Splash)

        self.mainLayout = QVBoxLayout(Splash)

        self.logo = QLabel()
        self.logo.setPixmap(SvgHelper.getQPixmapFromBytes(logoWhite, QSize(185.04,108.26)))
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(185.04, 108.26)
        self.logo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.logo.setAlignment(Qt.AlignCenter)

        self.title = QLabel()
        self.title.setText("淡江資訊處工讀考勤系統")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("微軟正黑體", 14))
        self.title.setStyleSheet("QLabel{color: white;}")
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.status = QLabel()
        self.status.setText("啟動中 請稍後")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont("微軟正黑體", 12))
        self.status.setStyleSheet("QLabel{color:white;}")

        self.mainLayout.addStretch(3)
        self.mainLayout.addWidget(self.logo, 4, Qt.AlignCenter)
        self.mainLayout.addStretch(3)
        self.mainLayout.addWidget(self.title, 1, Qt.AlignCenter)
        self.mainLayout.addWidget(self.status, 1, Qt.AlignCenter)
        self.mainLayout.addStretch(3)

    def retranslateUi(self, Splash):
        _translate = QCoreApplication.translate
        Splash.setWindowTitle(_translate("Splash", "淡江資訊處 工讀考勤系統"))
        Splash.setWindowIcon(QIcon(SvgHelper.getQPixmapFromBytes(logoIcon, QSize(512,512))))
