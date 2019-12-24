from UI_OffensiveEditor import Ui_OffensiveEditor
from PyQt5.QtWidgets import  QApplication, QMainWindow, QFrame, QMessageBox, QAction
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
import sys
import json
import itertools
from scoutcardmaker.Offense import Formation, PersonnelLabelMapper, OffenseLibrary


class FormationFrame(QFrame):
    TOP_LEFT = (50, 20)
    HOR_YD_LEN = 10
    VER_YD_LEN = 25
    HASH_SIZE = 6
    OFF_PLAYER_START = (TOP_LEFT[0] + HOR_YD_LEN * 54, TOP_LEFT[1] + VER_YD_LEN * 16)
    OFF_PLAYER_SIZE = (27, 22)


    @staticmethod
    def off_player_coords_to_canvas(x, y):
        return FormationFrame.OFF_PLAYER_START[0] + x * FormationFrame.HOR_YD_LEN, FormationFrame.OFF_PLAYER_START[1] + y * FormationFrame.VER_YD_LEN

    @staticmethod
    def canvas_coords_to_off_player(x, y):
        return (x - FormationFrame.OFF_PLAYER_START[0]) // FormationFrame.HOR_YD_LEN, (y - FormationFrame.OFF_PLAYER_START[1]) // FormationFrame.VER_YD_LEN

    @staticmethod
    def nearest_off_player_coord(canvas_x, canvas_y):
        return (canvas_x + FormationFrame.HOR_YD_LEN // 2 - FormationFrame.OFF_PLAYER_START[0]) // FormationFrame.HOR_YD_LEN, \
               (canvas_y + FormationFrame.VER_YD_LEN // 2 - FormationFrame.OFF_PLAYER_START[1]) // FormationFrame.VER_YD_LEN

    def __init__(self, formation, personnel_mapper):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setMinimumWidth(FormationFrame.TOP_LEFT[0] + FormationFrame.HOR_YD_LEN * 108 + 20)
        self.setMinimumHeight(FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 25 + 20)
        self.setStyleSheet("background-color: white;")
        self.formation = formation
        self.current_subformation_key = "MOF_RT"
        self.personnel_mapper = personnel_mapper
        self.selected_player = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))
        self.draw_field(painter)
        self.draw_subformation(painter)

    def draw_field(self, painter):
        painter.drawLine(FormationFrame.TOP_LEFT[0], FormationFrame.TOP_LEFT[1],
                         FormationFrame.TOP_LEFT[0], FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 25)
        painter.drawLine(FormationFrame.TOP_LEFT[0] + FormationFrame.HOR_YD_LEN * 108, FormationFrame.TOP_LEFT[1],
                         FormationFrame.TOP_LEFT[0] + FormationFrame.HOR_YD_LEN * 108, FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 25)
        for row in range(6):
            painter.drawLine(FormationFrame.TOP_LEFT[0], FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 5 * row,
                             FormationFrame.TOP_LEFT[0] + FormationFrame.HOR_YD_LEN * 108, FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 5 * row)

        for combo in list(itertools.product([14, 18, 36, 72, 90, 94],[0, 1, 2, 3, 4, 5])):
            offset = combo[0]
            row = combo[1]
            painter.drawLine(FormationFrame.TOP_LEFT[0] + FormationFrame.HOR_YD_LEN * offset,
                             FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 5 * row - FormationFrame.HASH_SIZE / 2,
                             FormationFrame.TOP_LEFT[0] + FormationFrame.HOR_YD_LEN * offset,
                             FormationFrame.TOP_LEFT[1] + FormationFrame.VER_YD_LEN * 5 * row + FormationFrame.HASH_SIZE / 2)

    def draw_subformation(self, painter):
        for player in self.formation.subformations[self.current_subformation_key].players.values():
            painter.drawEllipse(FormationFrame.OFF_PLAYER_START[0] + player.x * FormationFrame.HOR_YD_LEN - FormationFrame.OFF_PLAYER_SIZE[0] / 2,
                                FormationFrame.OFF_PLAYER_START[1] + player.y * FormationFrame.VER_YD_LEN - FormationFrame.OFF_PLAYER_SIZE[1] / 2,
                                FormationFrame.OFF_PLAYER_SIZE[0], FormationFrame.OFF_PLAYER_SIZE[1])
            painter.drawText(
                FormationFrame.OFF_PLAYER_START[0] + player.x * FormationFrame.HOR_YD_LEN - FormationFrame.OFF_PLAYER_SIZE[0] / 2,
                FormationFrame.OFF_PLAYER_START[1] + player.y * FormationFrame.VER_YD_LEN - FormationFrame.OFF_PLAYER_SIZE[1] / 2,
                FormationFrame.OFF_PLAYER_SIZE[0], FormationFrame.OFF_PLAYER_SIZE[1], Qt.AlignCenter, self.personnel_mapper.get_label(player.tag))

    def mousePressEvent(self, event):
        click_x, click_y = event.x(), event.y()
        x, y = FormationFrame.nearest_off_player_coord(click_x, click_y)

        for player in self.formation.subformations[self.current_subformation_key].players.values():
            if abs(player.x - x) <= 1 and player.y == y:
                self.selected_player = player
                break

    def mouseMoveEvent(self, event):
        mouse_x, mouse_y= event.x(), event.y()
        x, y = FormationFrame.nearest_off_player_coord(mouse_x, mouse_y)

        if self.selected_player:
            self.selected_player.x, self.selected_player.y = x, y
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
        self.formation_frame = FormationFrame(self.modifying_formation, self.formation_library.label_mappers['default'])
        self.scrollArea_2.setWidget(self.formation_frame)
        self.show()

        self.rb_mof.setChecked(True)
        self.rb_mof.clicked.connect(lambda : self.handle_view_change('MOF_RT'))
        self.rb_field.clicked.connect(lambda : self.handle_view_change('LH_RT'))
        self.rb_boundary.clicked.connect(lambda : self.handle_view_change('RH_RT'))

        self.list_formations.itemClicked.connect(self.handle_formation_clicked)
        self.edit_formation_name.returnPressed.connect(self.handle_save_formation)
        self.btn_save_formation.clicked.connect(self.handle_save_formation)

        self.actionSave_Library.triggered.connect(self.handle_save_library)

        self.init_label_mappers()
        self.combo_personnel_grouping.currentIndexChanged[str].connect(self.handle_personnel_change)
        self.set_personnel_cb_text(self.formation_library.label_mappers['default'].mappings)

    def handle_view_change(self, new_view_tag):
        self.formation_frame.current_subformation_key = new_view_tag
        self.formation_frame.update()

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
        self.formation_library.save_formation(self.modifying_formation, formation_name)
        self.load_formation_names_into_list()

    def load_formation_names_into_list(self):
        formation_names = [name for name in self.formation_library.formations.keys()]
        formation_names.sort()
        self.list_formations.clear()

        for formation_name in formation_names:
            self.list_formations.addItem(formation_name)

    def handle_formation_clicked(self, formation_clicked):
        formation_name = formation_clicked.data(0)
        self.edit_formation_name.setText(formation_name)
        self.modifying_formation.copy_from(self.formation_library.formations[formation_name])
        self.formation_frame.formation = self.modifying_formation
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
        with open('library.json', 'w') as file:
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



app = QApplication(sys.argv)
window = OffensiveLibraryEditor()

try:
    with open('library.json', 'r') as file:
        window.load_library_from_dict(json.load(file))
except FileNotFoundError:
    pass

sys.exit(app.exec_())