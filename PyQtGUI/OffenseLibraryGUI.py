from UI_OffensiveEditor import Ui_OffensiveEditor
from PyQt5.QtWidgets import  QApplication, QMainWindow, QFrame, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import sys
import itertools

from scoutcardmaker.Offense import Subformation
test_subformation_positions ={'L1': (-8, 0),
            'L3': (-4, 0),
            'L2': (4, 0),
            'L4': (8, 0),
            'C': (0, 0),
            'S1': (0, 1),
            'S2': (0, 5),
            'S3': (0, 7),
            'S4': (12, 0),
            'S5': (20, 0),
            'S6': (-20, 0)}
test_subformation = Subformation()
for player in test_subformation.players:
    player.x, player.y = test_subformation_positions[player.tag]


class Canvas(QFrame):
    TOP_LEFT = (50, 20)
    HOR_YD_LEN = 10
    VER_YD_LEN = 25
    HASH_SIZE = 6
    OFF_PLAYER_START = (TOP_LEFT[0] + HOR_YD_LEN * 54, TOP_LEFT[1] + VER_YD_LEN * 16)
    OFF_PLAYER_SIZE = (27, 22)


    @staticmethod
    def off_player_coords_to_canvas(x, y):
        return Canvas.OFF_PLAYER_START[0] + x * Canvas.HOR_YD_LEN, Canvas.OFF_PLAYER_START[1] + y * Canvas.VER_YD_LEN

    @staticmethod
    def canvas_coords_to_off_player(x, y):
        return (x - Canvas.OFF_PLAYER_START[0]) / Canvas.HOR_YD_LEN, (y - Canvas.OFF_PLAYER_START[1]) / Canvas.VER_YD_LEN

    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,600,600)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        self.setStyleSheet("background-color: white;")
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_field(painter)
        self.draw_subformation(painter, test_subformation)

    def draw_field(self, painter):
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(Canvas.TOP_LEFT[0], Canvas.TOP_LEFT[1],
                         Canvas.TOP_LEFT[0], Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 25)
        painter.drawLine(Canvas.TOP_LEFT[0] + Canvas.HOR_YD_LEN * 108, Canvas.TOP_LEFT[1],
                         Canvas.TOP_LEFT[0] + Canvas.HOR_YD_LEN * 108, Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 25)
        for row in range(6):
            painter.drawLine(Canvas.TOP_LEFT[0], Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 5 * row,
                             Canvas.TOP_LEFT[0] + Canvas.HOR_YD_LEN * 108, Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 5 * row)

        for combo in list(itertools.product([14, 18, 36, 72, 90, 94],[0, 1, 2, 3, 4, 5])):
            offset = combo[0]
            row = combo[1]
            painter.drawLine(Canvas.TOP_LEFT[0] + Canvas.HOR_YD_LEN * offset,
                             Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 5 * row - Canvas.HASH_SIZE / 2,
                             Canvas.TOP_LEFT[0] + Canvas.HOR_YD_LEN * offset,
                             Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 5 * row + Canvas.HASH_SIZE / 2)

    def draw_subformation(self, painter, sub_formation):
        print(sub_formation)
        for player in sub_formation.players:
            painter.drawEllipse(Canvas.OFF_PLAYER_START[0] + player.x * Canvas.HOR_YD_LEN - Canvas.OFF_PLAYER_SIZE[0] / 2,
                                 Canvas.OFF_PLAYER_START[1] + player.y * Canvas.VER_YD_LEN - Canvas.OFF_PLAYER_SIZE[1] / 2,
                                 Canvas.OFF_PLAYER_SIZE[0], Canvas.OFF_PLAYER_SIZE[1])
            painter.drawText(
                Canvas.OFF_PLAYER_START[0] + player.x * Canvas.HOR_YD_LEN - Canvas.OFF_PLAYER_SIZE[0] / 2,
                Canvas.OFF_PLAYER_START[1] + player.y * Canvas.VER_YD_LEN - Canvas.OFF_PLAYER_SIZE[1] / 2,
                Canvas.OFF_PLAYER_SIZE[0], Canvas.OFF_PLAYER_SIZE[1], Qt.AlignCenter, player.tag)


class OffensiveLibraryEditor(QMainWindow, Ui_OffensiveEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.canvas = Canvas()
        self.scrollArea_2.setWidget(self.canvas)
        self.show()


app = QApplication(sys.argv)
window = OffensiveLibraryEditor()
sys.exit(app.exec_())