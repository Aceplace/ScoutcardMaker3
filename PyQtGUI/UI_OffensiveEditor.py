# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\offense_editor.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OffensiveEditor(object):
    def setupUi(self, OffensiveEditor):
        OffensiveEditor.setObjectName("OffensiveEditor")
        OffensiveEditor.resize(1118, 733)
        self.central_widget = QtWidgets.QWidget(OffensiveEditor)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.splitter = QtWidgets.QSplitter(self.central_widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.edit_formation_name = QtWidgets.QLineEdit(self.widget)
        self.edit_formation_name.setObjectName("edit_formation_name")
        self.verticalLayout.addWidget(self.edit_formation_name)
        self.btn_save_formation = QtWidgets.QPushButton(self.widget)
        self.btn_save_formation.setObjectName("btn_save_formation")
        self.verticalLayout.addWidget(self.btn_save_formation)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.btn_delete_selected_formation = QtWidgets.QPushButton(self.widget)
        self.btn_delete_selected_formation.setObjectName("btn_delete_selected_formation")
        self.verticalLayout.addWidget(self.btn_delete_selected_formation)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 366, 548))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.list_formations = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.list_formations.setObjectName("list_formations")
        self.gridLayout.addWidget(self.list_formations, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget1)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.combo_personnel_grouping = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_personnel_grouping.setMinimumSize(QtCore.QSize(150, 0))
        self.combo_personnel_grouping.setObjectName("combo_personnel_grouping")
        self.horizontalLayout.addWidget(self.combo_personnel_grouping)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.cb_s1 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_s1.setObjectName("cb_s1")
        self.gridLayout_4.addWidget(self.cb_s1, 0, 0, 1, 1)
        self.cb_l4 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_l4.setObjectName("cb_l4")
        self.gridLayout_4.addWidget(self.cb_l4, 3, 1, 1, 1)
        self.cb_l1 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_l1.setObjectName("cb_l1")
        self.gridLayout_4.addWidget(self.cb_l1, 0, 1, 1, 1)
        self.cb_s4 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_s4.setObjectName("cb_s4")
        self.gridLayout_4.addWidget(self.cb_s4, 3, 0, 1, 1)
        self.cb_s2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_s2.setObjectName("cb_s2")
        self.gridLayout_4.addWidget(self.cb_s2, 1, 0, 1, 1)
        self.cb_l2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_l2.setObjectName("cb_l2")
        self.gridLayout_4.addWidget(self.cb_l2, 1, 1, 1, 1)
        self.cb_s3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_s3.setObjectName("cb_s3")
        self.gridLayout_4.addWidget(self.cb_s3, 2, 0, 1, 1)
        self.cb_l3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_l3.setObjectName("cb_l3")
        self.gridLayout_4.addWidget(self.cb_l3, 2, 1, 1, 1)
        self.cb_s6 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_s6.setObjectName("cb_s6")
        self.gridLayout_4.addWidget(self.cb_s6, 5, 0, 1, 1)
        self.cb_s5 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_s5.setObjectName("cb_s5")
        self.gridLayout_4.addWidget(self.cb_s5, 4, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.widget1)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rb_mof = QtWidgets.QRadioButton(self.groupBox)
        self.rb_mof.setObjectName("rb_mof")
        self.gridLayout_2.addWidget(self.rb_mof, 0, 0, 1, 1)
        self.rb_composite_mof = QtWidgets.QRadioButton(self.groupBox)
        self.rb_composite_mof.setObjectName("rb_composite_mof")
        self.gridLayout_2.addWidget(self.rb_composite_mof, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)
        self.rb_field = QtWidgets.QRadioButton(self.groupBox)
        self.rb_field.setObjectName("rb_field")
        self.gridLayout_2.addWidget(self.rb_field, 1, 0, 1, 1)
        self.rb_composite_lh = QtWidgets.QRadioButton(self.groupBox)
        self.rb_composite_lh.setObjectName("rb_composite_lh")
        self.gridLayout_2.addWidget(self.rb_composite_lh, 1, 1, 1, 1)
        self.edit_composite = QtWidgets.QLineEdit(self.groupBox)
        self.edit_composite.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_composite.sizePolicy().hasHeightForWidth())
        self.edit_composite.setSizePolicy(sizePolicy)
        self.edit_composite.setMinimumSize(QtCore.QSize(150, 0))
        self.edit_composite.setObjectName("edit_composite")
        self.gridLayout_2.addWidget(self.edit_composite, 1, 2, 1, 1)
        self.rb_boundary = QtWidgets.QRadioButton(self.groupBox)
        self.rb_boundary.setObjectName("rb_boundary")
        self.gridLayout_2.addWidget(self.rb_boundary, 2, 0, 1, 1)
        self.rb_composite_rh = QtWidgets.QRadioButton(self.groupBox)
        self.rb_composite_rh.setObjectName("rb_composite_rh")
        self.gridLayout_2.addWidget(self.rb_composite_rh, 2, 1, 1, 1)
        self.btn_load_composite = QtWidgets.QPushButton(self.groupBox)
        self.btn_load_composite.setObjectName("btn_load_composite")
        self.gridLayout_2.addWidget(self.btn_load_composite, 2, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.widget1)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.widget_formation_visualization = QtWidgets.QWidget()
        self.widget_formation_visualization.setGeometry(QtCore.QRect(0, 0, 721, 465))
        self.widget_formation_visualization.setStyleSheet("background-color: white;")
        self.widget_formation_visualization.setObjectName("widget_formation_visualization")
        self.scrollArea_2.setWidget(self.widget_formation_visualization)
        self.verticalLayout_3.addWidget(self.scrollArea_2)
        self.gridLayout_6.addWidget(self.splitter, 0, 0, 1, 1)
        OffensiveEditor.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(OffensiveEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1118, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        OffensiveEditor.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OffensiveEditor)
        self.statusbar.setObjectName("statusbar")
        OffensiveEditor.setStatusBar(self.statusbar)
        self.actionSave_Library = QtWidgets.QAction(OffensiveEditor)
        self.actionSave_Library.setObjectName("actionSave_Library")
        self.actionExit = QtWidgets.QAction(OffensiveEditor)
        self.actionExit.setObjectName("actionExit")
        self.menu_file.addAction(self.actionSave_Library)
        self.menu_file.addAction(self.actionExit)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(OffensiveEditor)
        self.actionExit.triggered.connect(OffensiveEditor.close)
        QtCore.QMetaObject.connectSlotsByName(OffensiveEditor)

    def retranslateUi(self, OffensiveEditor):
        _translate = QtCore.QCoreApplication.translate
        OffensiveEditor.setWindowTitle(_translate("OffensiveEditor", "MainWindow"))
        self.label.setText(_translate("OffensiveEditor", "Formation Name:"))
        self.btn_save_formation.setText(_translate("OffensiveEditor", "Save Formation"))
        self.label_2.setText(_translate("OffensiveEditor", "Formations"))
        self.btn_delete_selected_formation.setText(_translate("OffensiveEditor", "Delete Selected Formation"))
        self.groupBox_2.setTitle(_translate("OffensiveEditor", "Affected Personnel"))
        self.label_4.setText(_translate("OffensiveEditor", "Personnel Groupings:"))
        self.cb_s1.setText(_translate("OffensiveEditor", "S1"))
        self.cb_l4.setText(_translate("OffensiveEditor", "L4"))
        self.cb_l1.setText(_translate("OffensiveEditor", "L1"))
        self.cb_s4.setText(_translate("OffensiveEditor", "S4"))
        self.cb_s2.setText(_translate("OffensiveEditor", "S2"))
        self.cb_l2.setText(_translate("OffensiveEditor", "L2"))
        self.cb_s3.setText(_translate("OffensiveEditor", "S3"))
        self.cb_l3.setText(_translate("OffensiveEditor", "L3"))
        self.cb_s6.setText(_translate("OffensiveEditor", "S6"))
        self.cb_s5.setText(_translate("OffensiveEditor", "S5"))
        self.groupBox.setTitle(_translate("OffensiveEditor", "View"))
        self.rb_mof.setText(_translate("OffensiveEditor", "MOF"))
        self.rb_composite_mof.setText(_translate("OffensiveEditor", "Composite MOF"))
        self.label_5.setText(_translate("OffensiveEditor", "Composite Name"))
        self.rb_field.setText(_translate("OffensiveEditor", "Field"))
        self.rb_composite_lh.setText(_translate("OffensiveEditor", "Composite LH"))
        self.rb_boundary.setText(_translate("OffensiveEditor", "Boundary"))
        self.rb_composite_rh.setText(_translate("OffensiveEditor", "Composite RH"))
        self.btn_load_composite.setText(_translate("OffensiveEditor", "Load Composite"))
        self.menu_file.setTitle(_translate("OffensiveEditor", "File"))
        self.actionSave_Library.setText(_translate("OffensiveEditor", "Save Library"))
        self.actionExit.setText(_translate("OffensiveEditor", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OffensiveEditor = QtWidgets.QMainWindow()
    ui = Ui_OffensiveEditor()
    ui.setupUi(OffensiveEditor)
    OffensiveEditor.show()
    sys.exit(app.exec_())