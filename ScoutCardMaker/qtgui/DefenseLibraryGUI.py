from qtgui.UI_DefensiveEditor import Ui_DefensiveEditor
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
OFF_PLAYER_START = (TOP_LEFT[0] + HOR_YD_LEN * 54, TOP_LEFT[1] + VER_YD_LEN * 15)
OFF_PLAYER_SIZE = (27, 18)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class DefenseFrame(QFrame):
    def __init__(self, subformation, personnel_mapper):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setMinimumWidth(TOP_LEFT[0] + HOR_YD_LEN * 108 + 20)
        self.setMinimumHeight(TOP_LEFT[1] + VER_YD_LEN * 39 + 20)
        self.setStyleSheet("background-color: white;")
        self.offensive_subformation = subformation
        self.can_edit = True
        self.personnel_mapper = personnel_mapper
        self.selected_player = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))
        self.draw_field(painter)
        self.draw_subformation(painter)


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

        for combo in list(itertools.product([14, 18, 36, 72, 90, 94], [0, 1, 2, 3, 4, 5])):
            offset = combo[0]
            row = combo[1]
            painter.drawLine(TOP_LEFT[0] + HOR_YD_LEN * offset,
                             TOP_LEFT[1] + VER_YD_LEN * 5 * row - HASH_SIZE / 2,
                             TOP_LEFT[0] + HOR_YD_LEN * offset,
                             TOP_LEFT[1] + VER_YD_LEN * 5 * row + HASH_SIZE / 2)


    def draw_subformation(self, painter):
        try:
            off_player_start = (OFF_PLAYER_START[0], OFF_PLAYER_START[1])
            for player in self.offensive_subformation.players.values():
                painter.drawEllipse(off_player_start[0] + player.x * HOR_YD_LEN - OFF_PLAYER_SIZE[0] / 2,
                                    off_player_start[1] + player.y * VER_YD_LEN - OFF_PLAYER_SIZE[1] / 2,
                                    OFF_PLAYER_SIZE[0], OFF_PLAYER_SIZE[1])
                painter.drawText(off_player_start[0] + player.x * HOR_YD_LEN - OFF_PLAYER_SIZE[0] / 2,
                                 off_player_start[1] + player.y * VER_YD_LEN - OFF_PLAYER_SIZE[1] / 2,
                                 OFF_PLAYER_SIZE[0], OFF_PLAYER_SIZE[1], Qt.AlignCenter,
                                 self.personnel_mapper.get_label(player.tag))
        except Exception as e:
            print(str(e))


class DefensiveLibraryEditor(QMainWindow, Ui_DefensiveEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formation_library = OffenseLibrary()
        self.selected_personnel_key = "default"

        self.current_hash = 'MOF'
        starting_formation = Formation()
        self.lh_subformation = starting_formation.subformations['LT_RT']
        self.rh_subformation = starting_formation.subformations['RT_RT']
        self.mof_subformation = starting_formation.subformations['MOF_RT']
        self.current_subformation = self.mof_subformation

        self.defense_frame = DefenseFrame(self.current_subformation,
                                          self.formation_library.label_mappers['default'])
        self.scrollArea_2.setWidget(self.defense_frame)
        self.show()

        self.rb_mof.setChecked(True)
        self.rb_mof.clicked.connect(lambda: self.handle_hash_change('MOF'))
        self.rb_lh.clicked.connect(lambda: self.handle_hash_change('LT'))
        self.rb_rh.clicked.connect(lambda: self.handle_hash_change('RT'))

        self.edit_formation_name.returnPressed.connect(self.handle_get_composite)
        self.btn_load_composite.clicked.connect(self.handle_get_composite)

    def load_offense_library_from_dict(self, library_dict):
        self.formation_library = OffenseLibrary.from_dict(library_dict)

    def handle_hash_change(self, hash_mark):
        try:
            self.current_hash = hash_mark
            if hash_mark == 'MOF':
                self.current_subformation = self.mof_subformation
            else:
                self.current_subformation = self.lh_subformation if hash_mark == 'LT' else self.rh_subformation
            self.defense_frame.offensive_subformation = self.current_subformation
            self.defense_frame.update()
        except Exception as e:
            print(str(e))

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

                    self.defense_frame.offensive_subformation = self.current_subformation
                    self.defense_frame.update()
        except Exception as e:
            from traceback import format_exc
            print(format_exc())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DefensiveLibraryEditor()

    try:
        with open('library.json', 'r') as file:
            window.load_offense_library_from_dict(json.load(file))
    except FileNotFoundError:
        pass

    sys.exit(app.exec_())