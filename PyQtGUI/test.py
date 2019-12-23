from UI_OffensiveEditor import Ui_OffensiveEditor
from PyQt5.QtWidgets import  QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import sys
import itertools

class Canvas(QWidget):
    TOP_LEFT = (50, 20)
    HOR_YD_LEN = 10
    VER_YD_LEN = 25
    HASH_SIZE = 6

    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,600,600)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        self.setStyleSheet("background-color: white;")
        self.setAutoFillBackground(True)





class OffensiveLibraryEditor(QMainWindow, Ui_OffensiveEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.canvas = Canvas()
        self.scrollArea_2.setWidget(self.canvas)
        self.show()


app = QApplication(sys.argv)
window = QDialog()
sys.exit(app.exec_())