from UI_OffensiveEditor import Ui_OffensiveEditor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
import sys
import json
import itertools
from scoutcardmaker.Offense import Formation, OffenseLibrary


TOP_LEFT = (50, 25)
HOR_YD_LEN = 10
VER_YD_LEN = 22
HASH_SIZE = 6
OFF_PLAYER_START = (TOP_LEFT[0] + HOR_YD_LEN * 54, TOP_LEFT[1])
OFF_PLAYER_SIZE = (27, 18)
NEXT_FIELD_OFFSET = VER_YD_LEN * 12


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class DefenseFrame(QFrame):
    @staticmethod
    def nearest_off_player_coord(canvas_x, canvas_y, field_number):
        return ((canvas_x + HOR_YD_LEN // 2 - OFF_PLAYER_START[0]) // HOR_YD_LEN,
                (canvas_y + VER_YD_LEN // 2 - (OFF_PLAYER_START[1] + NEXT_FIELD_OFFSET * field_number)) // VER_YD_LEN)

    def __init__(self, formation, personnel_mapper):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setMinimumWidth(TOP_LEFT[0] + HOR_YD_LEN * 108 + 20)
        self.setMinimumHeight(TOP_LEFT[1] + VER_YD_LEN * 39 + 20)
        self.setStyleSheet("background-color: white;")
        self.formation = formation
        self.can_edit = True
        self.personnel_mapper = personnel_mapper
        self.selected_player = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))
        self.draw_field(painter, 0, 'Middle of Field (Going Right)' if self.can_edit else 'Middle of Field')
        self.draw_field(painter, 1, 'Towards Field' if self.can_edit else 'Left Hash')
        self.draw_field(painter, 2, 'Towards Boundary' if self.can_edit else 'Right Hash')
        self.draw_subformation(painter, 0, "MOF_RT")
        self.draw_subformation(painter, 1, "LH_RT")
        self.draw_subformation(painter, 2, "RH_RT")

    def draw_field(self, painter, field_num, field_label):
        top_left = (TOP_LEFT[0], TOP_LEFT[1] + NEXT_FIELD_OFFSET * field_num)
        painter.drawLine(top_left[0], top_left[1], top_left[0], top_left[1] + VER_YD_LEN * 10)
        painter.drawLine(top_left[0] + HOR_YD_LEN * 108, top_left[1], top_left[0] + HOR_YD_LEN * 108,
                         top_left[1] + VER_YD_LEN * 10)
        for row in range(3):
            painter.drawLine(top_left[0], top_left[1] + VER_YD_LEN * 5 * row,
                             top_left[0] + HOR_YD_LEN * 108, top_left[1] + VER_YD_LEN * 5 * row)

        for combo in list(itertools.product([14, 18, 36, 72, 90, 94],[0, 1, 2])):
            offset = combo[0]
            row = combo[1]
            painter.drawLine(top_left[0] + HOR_YD_LEN * offset, top_left[1] + VER_YD_LEN * 5 * row - HASH_SIZE / 2,
                             top_left[0] + HOR_YD_LEN * offset, top_left[1] + VER_YD_LEN * 5 * row + HASH_SIZE / 2)

        painter.drawText(top_left[0], top_left[1] - VER_YD_LEN, 500, 40, Qt.AlignLeft, field_label)

    def draw_subformation(self, painter, field_num, hash_key):
        off_player_start = (OFF_PLAYER_START[0], OFF_PLAYER_START[1] + NEXT_FIELD_OFFSET * field_num)
        for player in self.formation.subformations[hash_key].players.values():
            painter.drawEllipse(off_player_start[0] + player.x * HOR_YD_LEN - OFF_PLAYER_SIZE[0] / 2,
                                off_player_start[1] + player.y * VER_YD_LEN - OFF_PLAYER_SIZE[1] / 2,
                                OFF_PLAYER_SIZE[0], OFF_PLAYER_SIZE[1])
            painter.drawText(off_player_start[0] + player.x * HOR_YD_LEN - OFF_PLAYER_SIZE[0] / 2,
                             off_player_start[1] + player.y * VER_YD_LEN - OFF_PLAYER_SIZE[1] / 2,
                             OFF_PLAYER_SIZE[0], OFF_PLAYER_SIZE[1], Qt.AlignCenter,
                             self.personnel_mapper.get_label(player.tag))


class DefensiveLibraryEditor(QMainWindow, Ui_OffensiveEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formation_library = OffenseLibrary()
        self.selected_personnel_key = "default"
        self.modifying_formation = Formation()
        self.composite_formation = Formation()
        self.formation_frame = DefenseFrame(self.modifying_formation, self.formation_library.label_mappers['default'])
        self.scrollArea_2.setWidget(self.formation_frame)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DefensiveLibraryEditor()

    try:
        with open('library.json', 'r') as file:
            window.load_library_from_dict(json.load(file))
    except FileNotFoundError:
        pass

    sys.exit(app.exec_())