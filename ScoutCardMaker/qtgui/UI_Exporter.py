# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_exporter.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExportGui(object):
    def setupUi(self, ExportGui):
        ExportGui.setObjectName("ExportGui")
        ExportGui.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ExportGui)
        self.centralwidget.setObjectName("centralwidget")
        self.cb_college_hash_marks = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_college_hash_marks.setGeometry(QtCore.QRect(10, 10, 121, 17))
        self.cb_college_hash_marks.setObjectName("cb_college_hash_marks")
        ExportGui.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ExportGui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExports = QtWidgets.QMenu(self.menubar)
        self.menuExports.setObjectName("menuExports")
        ExportGui.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ExportGui)
        self.statusbar.setObjectName("statusbar")
        ExportGui.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(ExportGui)
        self.actionExit.setObjectName("actionExit")
        self.actionCreate_Scout_Cards = QtWidgets.QAction(ExportGui)
        self.actionCreate_Scout_Cards.setObjectName("actionCreate_Scout_Cards")
        self.actionCreate_Scout_Cards_Alternating = QtWidgets.QAction(ExportGui)
        self.actionCreate_Scout_Cards_Alternating.setObjectName("actionCreate_Scout_Cards_Alternating")
        self.action_Off_Create_Scout_Cards = QtWidgets.QAction(ExportGui)
        self.action_Off_Create_Scout_Cards.setObjectName("action_Off_Create_Scout_Cards")
        self.action_Off_Create_Scout_Cards_Alternating = QtWidgets.QAction(ExportGui)
        self.action_Off_Create_Scout_Cards_Alternating.setObjectName("action_Off_Create_Scout_Cards_Alternating")
        self.actionCreate_Football_Trainer_Script = QtWidgets.QAction(ExportGui)
        self.actionCreate_Football_Trainer_Script.setObjectName("actionCreate_Football_Trainer_Script")
        self.menuFile.addAction(self.actionExit)
        self.menuExports.addAction(self.actionCreate_Scout_Cards)
        self.menuExports.addAction(self.actionCreate_Scout_Cards_Alternating)
        self.menuExports.addAction(self.action_Off_Create_Scout_Cards)
        self.menuExports.addAction(self.action_Off_Create_Scout_Cards_Alternating)
        self.menuExports.addSeparator()
        self.menuExports.addAction(self.actionCreate_Football_Trainer_Script)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuExports.menuAction())

        self.retranslateUi(ExportGui)
        QtCore.QMetaObject.connectSlotsByName(ExportGui)

    def retranslateUi(self, ExportGui):
        _translate = QtCore.QCoreApplication.translate
        ExportGui.setWindowTitle(_translate("ExportGui", "MainWindow"))
        self.cb_college_hash_marks.setText(_translate("ExportGui", "College Hash Marks"))
        self.menuFile.setTitle(_translate("ExportGui", "File"))
        self.menuExports.setTitle(_translate("ExportGui", "Exports"))
        self.actionExit.setText(_translate("ExportGui", "Exit"))
        self.actionCreate_Scout_Cards.setText(_translate("ExportGui", "Create Scout Cards"))
        self.actionCreate_Scout_Cards_Alternating.setText(_translate("ExportGui", "Create Scout Cards Alternating"))
        self.action_Off_Create_Scout_Cards.setText(_translate("ExportGui", "(Off) Create Scout Cards"))
        self.action_Off_Create_Scout_Cards_Alternating.setText(_translate("ExportGui", "(Off) Create Scout Cards Alternating"))
        self.actionCreate_Football_Trainer_Script.setText(_translate("ExportGui", "Create Football Trainer Script"))
