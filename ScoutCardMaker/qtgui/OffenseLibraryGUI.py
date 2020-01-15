from qtgui.UI_OffensiveEditor import Ui_OffensiveEditor
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


class FormationFrame(QFrame):
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
        self.draw_subformation(painter, 1, "LT_RT")
        self.draw_subformation(painter, 2, "RT_RT")

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

    def mousePressEvent(self, event):
        if not self.can_edit:
            return
        click_x, click_y = event.x(), event.y()
        x0, y0 = FormationFrame.nearest_off_player_coord(click_x, click_y, 0)
        x1, y1 = FormationFrame.nearest_off_player_coord(click_x, click_y, 1)
        x2, y2 = FormationFrame.nearest_off_player_coord(click_x, click_y, 2)

        for player in self.formation.subformations["MOF_RT"].players.values():
            if abs(player.x - x0) <= 1 and player.y == y0:
                self.selected_player = (player, 0)
                break

        for player in self.formation.subformations["LT_RT"].players.values():
            if abs(player.x - x1) <= 1 and player.y == y1:
                self.selected_player = (player, 1)
                break

        for player in self.formation.subformations["RT_RT"].players.values():
            if abs(player.x - x2) <= 1 and player.y == y2:
                self.selected_player = (player, 2)
                break

    def mouseMoveEvent(self, event):
        if self.selected_player:
            mouse_x, mouse_y = event.x(), event.y()
            x, y = FormationFrame.nearest_off_player_coord(mouse_x, mouse_y, self.selected_player[1])

            self.selected_player[0].x, self.selected_player[0].y = x, y
            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_player = None


class OffensiveLibraryEditor(QMainWindow, Ui_OffensiveEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formation_library = OffenseLibrary()
        self.selected_personnel_key = "default"
        self.modifying_formation = Formation()
        self.composite_formation = Formation()
        self.formation_frame = FormationFrame(self.modifying_formation, self.formation_library.label_mappers['default'])
        self.scrollArea_2.setWidget(self.formation_frame)
        self.show()

        self.rb_editing.setChecked(True)
        self.rb_editing.clicked.connect(self.handle_editing_view_change)
        self.rb_composite.clicked.connect(self.handle_composite_view_change)
        self.edit_composite.returnPressed.connect(self.handle_get_composite)
        self.btn_load_composite.clicked.connect(self.handle_get_composite)

        self.list_formations.itemClicked.connect(self.handle_formation_clicked)
        self.edit_formation_name.returnPressed.connect(self.handle_save_formation)
        self.btn_save_formation.clicked.connect(self.handle_save_formation)
        self.btn_delete_selected_formation.clicked.connect(self.handle_delete_formation)

        self.actionSave_Library.triggered.connect(self.handle_save_library)

        self.init_label_mappers()
        self.combo_personnel_grouping.currentIndexChanged[str].connect(self.handle_personnel_change)
        self.set_personnel_cb_text(self.formation_library.label_mappers['default'].mappings)

    def handle_editing_view_change(self):
        self.formation_frame.can_edit = True
        self.formation_frame.formation = self.modifying_formation
        self.formation_frame.update()

    def handle_composite_view_change(self):
        self.formation_frame.can_edit = False
        self.formation_frame.formation = self.composite_formation
        self.formation_frame.update()

    def handle_get_composite(self):
        formation_name = self.edit_composite.text()
        #self.composite_formation = Formation()
        try:
            if len(formation_name) > 0:
                mof_composite = self.formation_library.get_composite_subformation('MOF', formation_name)[0]
                lh_composite = self.formation_library.get_composite_subformation('LH', formation_name)[0]
                rh_composite = self.formation_library.get_composite_subformation('RH', formation_name)[0]
                if not mof_composite is None:
                    self.composite_formation.subformations['MOF_RT'].copy_from(mof_composite)
                    self.composite_formation.subformations['LT_RT'].copy_from(lh_composite)
                    self.composite_formation.subformations['RT_RT'].copy_from(rh_composite)
                    self.formation_frame.update()
        except Exception as e:
            from traceback import format_exc
            print(format_exc())


    def handle_personnel_change(self, new_personnel):
        self.formation_frame.personnel_mapper = self.formation_library.label_mappers[new_personnel]
        self.set_personnel_cb_text(self.formation_library.label_mappers[new_personnel].mappings)
        self.formation_frame.update()

    def handle_save_formation(self):
        formation_name = self.edit_formation_name.text()
        if len(formation_name) == 0:
            msg_box = QMessageBox()
            msg_box.setText('Formation needs name')
            msg_box.setWindowTitle('Error')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        affected_tags = []
        if self.cb_l1.isChecked():
            affected_tags.append('L1')
        if self.cb_l2.isChecked():
            affected_tags.append('L2')
        if self.cb_l3.isChecked():
            affected_tags.append('L3')
        if self.cb_l4.isChecked():
            affected_tags.append('L4')
        if self.cb_s1.isChecked():
            affected_tags.append('S1')
        if self.cb_s2.isChecked():
            affected_tags.append('S2')
        if self.cb_s3.isChecked():
            affected_tags.append('S3')
        if self.cb_s4.isChecked():
            affected_tags.append('S4')
        if self.cb_s5.isChecked():
            affected_tags.append('S5')
        if self.cb_s6.isChecked():
            affected_tags.append('S6')

        self.modifying_formation.affected_tags = affected_tags
        self.formation_library.save_formation_from_going_rt(self.modifying_formation, formation_name)
        self.load_formation_names_into_list()

    def handle_delete_formation(self):
        if self.list_formations.currentItem():
            formation_name = self.list_formations.currentItem().text()

            del self.formation_library.formations[formation_name]
            self.load_formation_names_into_list()

    def load_formation_names_into_list(self):
        formation_names = [name for name in self.formation_library.formations.keys()]
        formation_names.sort()
        self.list_formations.clear()

        for formation_name in formation_names:
            self.list_formations.addItem(formation_name)

    def handle_formation_clicked(self, formation_clicked):
        formation_name = formation_clicked.data(0)
        self.rb_editing.setChecked(True)
        self.edit_formation_name.setText(formation_name)
        self.modifying_formation.copy_from(self.formation_library.formations[formation_name])
        self.formation_frame.formation = self.modifying_formation
        self.formation_frame.can_edit = True
        self.formation_frame.update()

        self.cb_l1.setChecked(True if 'L1' in self.modifying_formation.affected_tags else False)
        self.cb_l2.setChecked(True if 'L2' in self.modifying_formation.affected_tags else False)
        self.cb_l3.setChecked(True if 'L3' in self.modifying_formation.affected_tags else False)
        self.cb_l4.setChecked(True if 'L4' in self.modifying_formation.affected_tags else False)
        self.cb_s1.setChecked(True if 'S1' in self.modifying_formation.affected_tags else False)
        self.cb_s2.setChecked(True if 'S2' in self.modifying_formation.affected_tags else False)
        self.cb_s3.setChecked(True if 'S3' in self.modifying_formation.affected_tags else False)
        self.cb_s4.setChecked(True if 'S4' in self.modifying_formation.affected_tags else False)
        self.cb_s5.setChecked(True if 'S5' in self.modifying_formation.affected_tags else False)
        self.cb_s6.setChecked(True if 'S6' in self.modifying_formation.affected_tags else False)

    def handle_save_library(self):
        with open('offense_library.json', 'w') as file:
            json.dump(self.formation_library.to_dict(), file, indent=3)

    def load_library_from_dict(self, library_dict):
        self.formation_library = OffenseLibrary.from_dict(library_dict)
        self.load_formation_names_into_list()
        self.init_label_mappers()

    def init_label_mappers(self):
        # Must block signals because clear sends index changed signal which then references the now empty(null) combo box
        self.combo_personnel_grouping.blockSignals(True)
        self.combo_personnel_grouping.clear()
        self.combo_personnel_grouping.blockSignals(False)

        for personnel_grouping_key in self.formation_library.label_mappers.keys():
            self.combo_personnel_grouping.addItem(personnel_grouping_key)

    def set_personnel_cb_text(self, personnel_mapping):
        self.cb_l1.setText(f'L1 ( {personnel_mapping["L1"]} )')
        self.cb_l2.setText(f'L2 ( {personnel_mapping["L2"]} )')
        self.cb_l3.setText(f'L3 ( {personnel_mapping["L3"]} )')
        self.cb_l4.setText(f'L4 ( {personnel_mapping["L4"]} )')
        self.cb_s1.setText(f'S1 ( {personnel_mapping["S1"]} )')
        self.cb_s2.setText(f'S2 ( {personnel_mapping["S2"]} )')
        self.cb_s3.setText(f'S3 ( {personnel_mapping["S3"]} )')
        self.cb_s4.setText(f'S4 ( {personnel_mapping["S4"]} )')
        self.cb_s5.setText(f'S5 ( {personnel_mapping["S5"]} )')
        self.cb_s6.setText(f'S6 ( {personnel_mapping["S6"]} )')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OffensiveLibraryEditor()

    try:
        with open('offense_library.json', 'r') as file:
            window.load_library_from_dict(json.load(file))
    except FileNotFoundError:
        print('File not found')

    sys.exit(app.exec_())