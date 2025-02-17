# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'watertrackerapp.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(374, 566)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 260, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Headline R")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(90, 140, 191, 91))
        self.textEdit.setAutoFillBackground(False)
#        self.textEdit.setFrameShape(QtWidgets.QFrame.Box)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(110, 320, 141, 31))
        self.textEdit_2.setAutoFillBackground(True)
#        self.textEdit_2.setFrameShape(QtWidgets.QFrame.NoFrame)
#        self.textEdit_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit_2.setLineWidth(0)
        self.textEdit_2.setObjectName("textEdit_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 30, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)
#        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.Panel)
#        self.plainTextEdit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 374, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Water Status Tracker"))
        self.pushButton.setText(_translate("MainWindow", "Water Status"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Last Tracked: </p></body></html>"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "  Water Status Tracker App"))



#
# from PyQt6 import QtCore, QtGui, QtWidgets
#
#
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(374, 566)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(100, 260, 161, 51))
#         font = QtGui.QFont()
#         font.setFamily("Headline R")
#         font.setPointSize(10)
#         self.pushButton.setFont(font)
#         self.pushButton.setCheckable(True)
#         self.pushButton.setObjectName("pushButton")
#         self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit.setGeometry(QtCore.QRect(90, 140, 191, 91))
#         self.textEdit.setAutoFillBackground(False)
# #        self.textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
#         self.textEdit.setObjectName("textEdit")
#         self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
#         self.textEdit_2.setGeometry(QtCore.QRect(110, 320, 141, 31))
#         self.textEdit_2.setAutoFillBackground(True)
# #        self.textEdit_2.setFrameShape(QtWidgets.QFrame.NoFrame)
# #        self.textEdit_2.setFrameShadow(QtWidgets.QFrame.Plain)
#         self.textEdit_2.setLineWidth(0)
#         self.textEdit_2.setObjectName("textEdit_2")
#         self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
#         self.plainTextEdit.setGeometry(QtCore.QRect(50, 30, 291, 41))
#         font = QtGui.QFont()
#         font.setFamily("Sitka")
#         font.setPointSize(12)
#         self.plainTextEdit.setFont(font)
# #        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.Panel)
# #        self.plainTextEdit.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.plainTextEdit.setObjectName("plainTextEdit")
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 374, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "Water Status Tracker"))
#         self.pushButton.setText(_translate("MainWindow", "Water Status"))
#         self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
#         self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Last Tracked: </p></body></html>"))
#         self.plainTextEdit.setPlainText(_translate("MainWindow", "  Water Status Tracker App"))
