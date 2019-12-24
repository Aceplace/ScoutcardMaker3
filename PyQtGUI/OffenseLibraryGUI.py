from UI_OffensiveEditor import Ui_OffensiveEditor
from PyQt5.QtWidgets import  QApplication, QMainWindow, QFrame, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
import sys
import itertools
from scoutcardmaker.Offense import Formation, PersonnelLabelMapper


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
        return (x - Canvas.OFF_PLAYER_START[0]) // Canvas.HOR_YD_LEN, (y - Canvas.OFF_PLAYER_START[1]) // Canvas.VER_YD_LEN

    @staticmethod
    def nearest_off_player_coord(canvas_x, canvas_y):
        return (canvas_x + Canvas.HOR_YD_LEN // 2 - Canvas.OFF_PLAYER_START[0]) // Canvas.HOR_YD_LEN, \
               (canvas_y + Canvas.VER_YD_LEN // 2 - Canvas.OFF_PLAYER_START[1]) // Canvas.VER_YD_LEN

    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setMinimumWidth(Canvas.TOP_LEFT[0] + Canvas.HOR_YD_LEN * 108 + 20)
        self.setMinimumHeight(Canvas.TOP_LEFT[1] + Canvas.VER_YD_LEN * 25 + 20)
        self.setStyleSheet("background-color: white;")
        self.formation = Formation()
        self.current_subformation_key = "MOF_RT"
        self.personnel_mapper = PersonnelLabelMapper()
        self.selected_player = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))
        self.draw_field(painter)
        self.draw_subformation(painter)

    def draw_field(self, painter):
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

    def draw_subformation(self, painter):
        for player in self.formation.subformations[self.current_subformation_key].players.values():
            painter.drawEllipse(Canvas.OFF_PLAYER_START[0] + player.x * Canvas.HOR_YD_LEN - Canvas.OFF_PLAYER_SIZE[0] / 2,
                                 Canvas.OFF_PLAYER_START[1] + player.y * Canvas.VER_YD_LEN - Canvas.OFF_PLAYER_SIZE[1] / 2,
                                 Canvas.OFF_PLAYER_SIZE[0], Canvas.OFF_PLAYER_SIZE[1])
            painter.drawText(
                Canvas.OFF_PLAYER_START[0] + player.x * Canvas.HOR_YD_LEN - Canvas.OFF_PLAYER_SIZE[0] / 2,
                Canvas.OFF_PLAYER_START[1] + player.y * Canvas.VER_YD_LEN - Canvas.OFF_PLAYER_SIZE[1] / 2,
                Canvas.OFF_PLAYER_SIZE[0], Canvas.OFF_PLAYER_SIZE[1], Qt.AlignCenter, self.personnel_mapper.get_label(player.tag))

    def mousePressEvent(self, event):
        click_x, click_y = event.x(), event.y()
        x, y = Canvas.nearest_off_player_coord(click_x, click_y)

        for player in self.formation.subformations[self.current_subformation_key].players.values():
            if abs(player.x - x) <= 1 and player.y == y:
                self.selected_player = player
                break

    def mouseMoveEvent(self, event):
        mouse_x, mouse_y= event.x(), event.y()
        x, y = Canvas.nearest_off_player_coord(mouse_x, mouse_y)

        if self.selected_player:
            self.selected_player.x, self.selected_player.y = x, y
            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_player = None



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