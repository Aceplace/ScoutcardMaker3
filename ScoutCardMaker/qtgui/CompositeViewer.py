from qtgui.UI_CompositeViewer import Ui_CompositeViewer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLineEdit, QWidget, QPushButton, QHBoxLayout, \
    QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt
import sys
import json
import itertools
from scoutcardmaker.Offense import Formation, OffenseLibrary
from scoutcardmaker.Defense import Defense, DefenseLibrary
from scoutcardmaker.Utils import PersonnelLabelMapper, INVALID_POSITION


TOP_LEFT = (50, 25)
HOR_YD_LEN = 10
VER_YD_LEN = 22
HASH_SIZE = 6
PLAYER_START = (TOP_LEFT[0] + HOR_YD_LEN * 54, TOP_LEFT[1] + VER_YD_LEN * 15)
OFF_PLAYER_SIZE = (27, 18)
DEF_PLAYER_SIZE = (30, 30)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class DefenseVisualFrame(QFrame):
    def __init__(self, subformation, defense, defense_personnel_mapper):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setMinimumWidth(TOP_LEFT[0] + HOR_YD_LEN * 108 + 20)
        self.setMinimumHeight(TOP_LEFT[1] + VER_YD_LEN * 39 + 20)
        self.setStyleSheet("background-color: white;")

        self.offensive_subformation = subformation
        self.defense = defense
        self.defense_personnel_mapper = defense_personnel_mapper
        self.offense_personnel_mapper = PersonnelLabelMapper('offense')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))
        self.draw_field(painter)
        font = QFont()
        font.setPixelSize(14)
        painter.setFont(font)
        self.draw_subformation(painter)
        font.setPixelSize(24)
        painter.setFont(font)
        self.draw_defense(painter)

    def draw_field(self, painter):
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(TOP_LEFT[0], TOP_LEFT[1],
                         TOP_LEFT[0], TOP_LEFT[1] + VER_YD_LEN * 25)
        painter.drawLine(TOP_LEFT[0] + HOR_YD_LEN * 108, TOP_LEFT[1],
                         TOP_LEFT[0] + HOR_YD_LEN * 108, TOP_LEFT[1] + VER_YD_LEN * 25)
        for row in range(6):
            painter.drawLine(TOP_LEFT[0], TOP_LEFT[1] + VER_YD_LEN * 5 * row,
                             TOP_LEFT[0] + HOR_YD_LEN * 108,
                             TOP_LEFT[1] + VER_YD_LEN * 5 * row)

        for combo in list(itertools.product([14, 18, 36, 42, 66, 72, 90, 94], [0, 1, 2, 3, 4, 5])):
            offset = combo[0]
            row = combo[1]
            painter.drawLine(TOP_LEFT[0] + HOR_YD_LEN * offset,
                             TOP_LEFT[1] + VER_YD_LEN * 5 * row - HASH_SIZE / 2,
                             TOP_LEFT[0] + HOR_YD_LEN * offset,
                             TOP_LEFT[1] + VER_YD_LEN * 5 * row + HASH_SIZE / 2)

    def draw_subformation(self, painter):
        player_start = (PLAYER_START[0], PLAYER_START[1])
        for player in self.offensive_subformation.players.values():
            painter.drawEllipse(player_start[0] + player.x * HOR_YD_LEN - OFF_PLAYER_SIZE[0] / 2,
                                player_start[1] + player.y * VER_YD_LEN - OFF_PLAYER_SIZE[1] / 2,
                                OFF_PLAYER_SIZE[0], OFF_PLAYER_SIZE[1])
            painter.drawText(player_start[0] + player.x * HOR_YD_LEN - OFF_PLAYER_SIZE[0] / 2,
                             player_start[1] + player.y * VER_YD_LEN - OFF_PLAYER_SIZE[1] / 2,
                             OFF_PLAYER_SIZE[0], OFF_PLAYER_SIZE[1], Qt.AlignCenter,
                             self.offense_personnel_mapper.get_label(player.tag))

    def draw_defense(self, painter):
        player_start = (PLAYER_START[0], PLAYER_START[1])
        self.defense.place_defenders(self.offensive_subformation)
        for defender in self.defense.players.values():
            if defender.tag not in self.defense.affected_tags:
                continue
            if defender.placed_x == INVALID_POSITION[0] and defender.placed_y == INVALID_POSITION[1]:
                continue
            try:
                painter.drawText(player_start[0] + defender.placed_x * HOR_YD_LEN - DEF_PLAYER_SIZE[0] / 2,
                                 player_start[1] - defender.placed_y * VER_YD_LEN - DEF_PLAYER_SIZE[0] / 2,
                                 DEF_PLAYER_SIZE[0], DEF_PLAYER_SIZE[1], Qt.AlignCenter,
                                 self.defense_personnel_mapper.get_label(defender.tag))
            except Exception:
                import traceback
                traceback.print_exc()


class CompositeViewer(QMainWindow, Ui_CompositeViewer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formation_library = OffenseLibrary()
        self.defense_library = DefenseLibrary()

        self.current_hash = 'MOF'
        starting_formation = Formation()
        self.lh_subformation = starting_formation.subformations['LT_RT']
        self.rh_subformation = starting_formation.subformations['RT_RT']
        self.mof_subformation = starting_formation.subformations['MOF_RT']
        self.current_subformation = self.mof_subformation

        self.current_defense = Defense()
        self.defense_visual_frame = DefenseVisualFrame(self.current_subformation, self.current_defense,
                                                       self.defense_library.label_mappers['default'])
        self.scroll_field.setWidget(self.defense_visual_frame)

        self.edit_formation_name.returnPressed.connect(self.handle_get_composite)
        self.btn_load_composite.clicked.connect(self.handle_get_composite)

        self.edit_defense_name.returnPressed.connect(self.handle_get_defense)
        self.btn_load_defense.clicked.connect(self.handle_get_composite)

        self.rb_lh.clicked.connect(lambda: self.handle_hash_change('LT'))
        self.rb_mof.clicked.connect(lambda: self.handle_hash_change('MOF'))
        self.rb_rh.clicked.connect(lambda: self.handle_hash_change('RT'))

        self.show()

    def load_offense_library_from_dict(self, library_dict):
        self.formation_library = OffenseLibrary.from_dict(library_dict)
        self.defense_visual_frame.offense_personnel_mapper = self.formation_library.label_mappers['default']

    def load_defense_library_from_dict(self, library_dict):
        self.defense_library = DefenseLibrary.from_dict(library_dict)
        self.defense_visual_frame.defense_personnel_mapper = self.defense_library.label_mappers['default']

    def handle_hash_change(self, hash_mark):
        try:
            self.current_hash = hash_mark
            if hash_mark == 'MOF':
                self.current_subformation = self.mof_subformation
            else:
                self.current_subformation = self.lh_subformation if hash_mark == 'LT' else self.rh_subformation
            self.defense_visual_frame.offensive_subformation = self.current_subformation
            self.defense_visual_frame.update()
        except Exception as e:
            from traceback import format_exc
            print(format_exc())

    def handle_get_composite(self):
        formation_name = self.edit_formation_name.text()
        try:
            if len(formation_name) > 0:
                mof_composite = self.formation_library.get_composite_subformation('MOF', formation_name)[0]
                lh_composite = self.formation_library.get_composite_subformation('LT', formation_name)[0]
                rh_composite = self.formation_library.get_composite_subformation('RT', formation_name)[0]
                if mof_composite is not None:
                    self.mof_subformation = mof_composite
                    self.lh_subformation = lh_composite
                    self.rh_subformation = rh_composite

                    if self.current_hash == 'MOF':
                        self.current_subformation = self.mof_subformation
                    else:
                        self.current_subformation = self.lh_subformation if self.current_hash == 'LT' else self.rh_subformation

                    self.defense_visual_frame.offensive_subformation = self.current_subformation
                    self.defense_visual_frame.update()
        except Exception as e:
            from traceback import format_exc
            print(format_exc())

    def handle_get_defense(self):
        defense_name = self.edit_defense_name.text()
        try:
            if len(defense_name) > 0:
                self.current_defense = self.defense_library.get_composite_defense(defense_name)
                self.defense_visual_frame.defense = self.current_defense
                self.defense_visual_frame.update()
        except Exception as e:
            from traceback import format_exc
            print(format_exc())


def launch():
    app = QApplication(sys.argv)
    window = CompositeViewer()

    window.setWindowTitle('Composite Viewer')

    try:
        with open('offense_library.json', 'r') as file:
            window.load_offense_library_from_dict(json.load(file))
    except FileNotFoundError:
        pass

    try:
        with open('defense_library.json', 'r') as file:
            window.load_defense_library_from_dict(json.load(file))
    except FileNotFoundError:
        pass

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
