from qtgui.UI_DefensiveEditor import Ui_DefensiveEditor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLineEdit, QWidget, QPushButton, QHBoxLayout, \
    QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
import sys
import json
import itertools
from scoutcardmaker.Offense import Formation, OffenseLibrary
from scoutcardmaker.Defense import Defense, DefenseLibrary, ConditionSet
from scoutcardmaker.LibraryUtils import PersonnelLabelMapper
from scoutcardmaker.FormationFunctions import formation_function_info
from scoutcardmaker.PlacementRules import placement_rule_info
from scoutcardmaker.DefenseParsers import DefensiveValidator

TOP_LEFT = (50, 25)
HOR_YD_LEN = 10
VER_YD_LEN = 22
HASH_SIZE = 6
OFF_PLAYER_START = (TOP_LEFT[0] + HOR_YD_LEN * 54, TOP_LEFT[1] + VER_YD_LEN * 15)
OFF_PLAYER_SIZE = (27, 18)


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class ConditionSetEditor(QWidget):
    def __init__(self, index, change_callback, delete_callback, add_callback, condition='', placement_rule=''):
        super().__init__()
        self.index = index
        self.edit_condition = QLineEdit()
        self.edit_placement_rule = QLineEdit()
        self.btn_delete_button = QPushButton('x')
        self.btn_delete_button.setMaximumWidth(32)
        self.btn_add_button = QPushButton('+')
        self.btn_add_button .setMaximumWidth(32)

        layout = QHBoxLayout(self)
        layout.addWidget(self.edit_condition)
        layout.addWidget(self.edit_placement_rule)
        layout.addWidget(self.btn_delete_button)
        layout.addWidget(self.btn_add_button)

        self.edit_condition.setText(condition)
        self.edit_placement_rule.setText(placement_rule)

        self.edit_condition.editingFinished.connect(lambda: change_callback(self.index, self.edit_condition.text(), self.edit_placement_rule.text()))
        self.edit_placement_rule.editingFinished.connect(lambda: change_callback(self.index, self.edit_condition.text(), self.edit_placement_rule.text()))

        self.btn_delete_button.pressed.connect(lambda: delete_callback(self.index))
        self.btn_add_button.pressed.connect(add_callback)


class DefenderEditor(QWidget):
    def __init__(self, status_bar):
        super().__init__()
        self.status_bar = status_bar
        self.condition_set_editors = []
        self.defender = None
        self.layout = None
        self.layout = QVBoxLayout(self)
        self.validator = DefensiveValidator(formation_function_info, placement_rule_info)

    def create_and_layout_condition_set_editors(self, defender):
        self.defender = defender
        condition_sets = self.defender.condition_sets
        for condition_set_editor in self.condition_set_editors:
            self.layout.removeWidget(condition_set_editor)
            condition_set_editor.deleteLater()

        self.condition_set_editors = []
        for index, condition_set in enumerate(condition_sets):
            condition_set_editor = ConditionSetEditor(index, self.edit_condition_set, self.delete_condition_set, self.add_condition_set,
                                                      condition_set.condition, condition_set.placement_rule)
            self.condition_set_editors.append(condition_set_editor)
            self.layout.addWidget(condition_set_editor)

    def edit_condition_set(self, index, condition, placement_rule):
        #validate
        invalid = False
        if not self.validator.validate_condition(condition):
            self.status_bar.showMessage(f'Condition Validation Error: {self.validator.error_message}', 7000)
            condition = ''
            invalid = True
        if not self.validator.validate_placement_rule(placement_rule):
            self.status_bar.showMessage(f'Placement Rule Validation Error: {self.validator.error_message}', 7000)
            placement_rule = ''
            invalid = True

        self.defender.condition_sets[index].condition = condition
        self.defender.condition_sets[index].placement_rule = placement_rule
        self.condition_set_editors[index].setStyleSheet(f'color: {"red" if invalid else "green"}')

    def add_condition_set(self):
        index = len(self.condition_set_editors)
        condition_set_editor = ConditionSetEditor(index, self.edit_condition_set, self.delete_condition_set, self.add_condition_set,
                                                  '', '')
        self.condition_set_editors.append(condition_set_editor)
        self.layout.addWidget(condition_set_editor)
        self.defender.condition_sets.append(ConditionSet())

    def delete_condition_set(self, index):
        if len(self.condition_set_editors) == 1:
            return

        self.layout.removeWidget(self.condition_set_editors[index])
        self.condition_set_editors[index].deleteLater()
        del self.condition_set_editors[index]
        del self.defender.condition_sets[index]

        for index, condition_set_editor in enumerate(self.condition_set_editors):
            condition_set_editor.index = index


class DefenseVisualFrame(QFrame):
    def __init__(self, subformation, defense_personnel_mapper):
        super().__init__()
        self.setGeometry(0,0,600,600)
        self.setMinimumWidth(TOP_LEFT[0] + HOR_YD_LEN * 108 + 20)
        self.setMinimumHeight(TOP_LEFT[1] + VER_YD_LEN * 39 + 20)
        self.setStyleSheet("background-color: white;")
        self.offensive_subformation = subformation
        self.can_edit = True
        self.defense_personnel_mapper = defense_personnel_mapper
        self.offense_personnel_mapper = PersonnelLabelMapper('offense')
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
                                 self.offense_personnel_mapper.get_label(player.tag))
        except Exception as e:
            from traceback import format_exc
            print(format_exc())


class DefensiveLibraryEditor(QMainWindow, Ui_DefensiveEditor):
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

        self.modifying_defense = Defense()
        self.defender_editor = DefenderEditor(self.statusBar())
        self.scroll_defender_edit.setWidget(self.defender_editor)
        self.defender_editor.create_and_layout_condition_set_editors(self.modifying_defense.players['D1'])

        self.init_label_mappers()
        self.init_defender_combo(self.defense_library.label_mappers['default'].mappings)
        self.combo_personnel_grouping.currentIndexChanged[str].connect(self.handle_personnel_change)
        self.combo_defender_to_edit.currentIndexChanged[str].connect(self.handle_defender_change)
        self.set_personnel_cb_text(self.defense_library.label_mappers['default'].mappings)
        self.btn_save_defense.clicked.connect(self.handle_save_defense)
        self.edit_defense_name.returnPressed.connect(self.handle_save_defense)
        self.list_defenses.itemClicked.connect(self.handle_defense_clicked)

        self.defense_frame = DefenseVisualFrame(self.current_subformation,
                                                self.formation_library.label_mappers['default'])
        self.scroll_field.setWidget(self.defense_frame)

        self.rb_mof.setChecked(True)
        self.rb_mof.clicked.connect(lambda: self.handle_hash_change('MOF'))
        self.rb_lh.clicked.connect(lambda: self.handle_hash_change('LT'))
        self.rb_rh.clicked.connect(lambda: self.handle_hash_change('RT'))
        self.edit_formation_name.returnPressed.connect(self.handle_get_composite)
        self.btn_load_composite.clicked.connect(self.handle_get_composite)

        self.actionSave_Library.triggered.connect(self.handle_save_library)

        self.show()

    def load_offense_library_from_dict(self, library_dict):
        self.formation_library = OffenseLibrary.from_dict(library_dict)

    def load_defense_library_from_dict(self, library_dict):
        self.defense_library = DefenseLibrary.from_dict(library_dict)
        self.init_label_mappers()
        self.load_defense_names_into_list()

    def handle_save_library(self):
        with open('defense_library.json', 'w') as file:
            json.dump(self.defense_library.to_dict(), file, indent=3)

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

                    self.defense_frame.offensive_subformation = self.current_subformation
                    self.defense_frame.update()
        except Exception as e:
            from traceback import format_exc
            print(format_exc())

    def init_label_mappers(self):
        # Must block signals because clear sends index changed signal which then references the now empty(null) combo box
        self.combo_personnel_grouping.blockSignals(True)
        self.combo_personnel_grouping.clear()
        self.combo_personnel_grouping.blockSignals(False)

        for personnel_grouping_key in self.defense_library.label_mappers.keys():
            self.combo_personnel_grouping.addItem(personnel_grouping_key)

    def handle_personnel_change(self, new_personnel):
        self.defense_frame.personnel_mapper = self.defense_library.label_mappers[new_personnel]
        self.set_personnel_cb_text(self.defense_library.label_mappers[new_personnel].mappings)
        self.defense_frame.update()

    def set_personnel_cb_text(self, personnel_mapping):
        self.cb_d1.setText(f'D1 ( {personnel_mapping["D1"]} )')
        self.cb_d2.setText(f'D2 ( {personnel_mapping["D2"]} )')
        self.cb_d3.setText(f'D3 ( {personnel_mapping["D3"]} )')
        self.cb_d4.setText(f'D4 ( {personnel_mapping["D4"]} )')
        self.cb_d5.setText(f'D5 ( {personnel_mapping["D5"]} )')
        self.cb_d6.setText(f'D6 ( {personnel_mapping["D6"]} )')
        self.cb_d7.setText(f'D7 ( {personnel_mapping["D7"]} )')
        self.cb_d8.setText(f'D8 ( {personnel_mapping["D8"]} )')
        self.cb_d9.setText(f'D9 ( {personnel_mapping["D9"]} )')
        self.cb_d10.setText(f'D10 ( {personnel_mapping["D10"]} )')
        self.cb_d11.setText(f'D11 ( {personnel_mapping["D11"]} )')

    def init_defender_combo(self, personnel_mapping):
        # Must block signals because clear sends index changed signal which then references the now empty(null) combo box
        self.combo_defender_to_edit.blockSignals(True)
        self.combo_defender_to_edit.clear()
        self.combo_defender_to_edit.blockSignals(False)

        for defender_tag in ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11']:
            self.combo_defender_to_edit.addItem(f'{defender_tag} ( {personnel_mapping[defender_tag]} )')

    def handle_defender_change(self, new_defender):
        new_defender_tag = new_defender.split()[0]
        current_defender = self.modifying_defense.players[new_defender_tag]
        self.defender_editor.create_and_layout_condition_set_editors(current_defender)

    def handle_save_defense(self):
        defense_name = self.edit_defense_name.text()
        if len(defense_name) == 0:
            msg_box = QMessageBox()
            msg_box.setText('Defense needs name')
            msg_box.setWindowTitle('Error')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        affected_tags = []
        if self.cb_d1.isChecked():
            affected_tags.append('D1')
        if self.cb_d2.isChecked():
            affected_tags.append('D2')
        if self.cb_d3.isChecked():
            affected_tags.append('D3')
        if self.cb_d4.isChecked():
            affected_tags.append('D4')
        if self.cb_d5.isChecked():
            affected_tags.append('D5')
        if self.cb_d6.isChecked():
            affected_tags.append('D6')
        if self.cb_d7.isChecked():
            affected_tags.append('D7')
        if self.cb_d8.isChecked():
            affected_tags.append('D8')
        if self.cb_d9.isChecked():
            affected_tags.append('D9')
        if self.cb_d10.isChecked():
            affected_tags.append('D10')
        if self.cb_d11.isChecked():
            affected_tags.append('D11')

        self.modifying_defense.affected_tags = affected_tags
        self.defense_library.save_defense(self.modifying_defense, defense_name)
        self.load_defense_names_into_list()

    def handle_delete_formation(self):
        if self.list_defenses.currentItem():
            defense_name = self.list_defenses.currentItem().text()

            del self.defense_library.defenses[defense_name]
            self.load_defense_names_into_list()

    def load_defense_names_into_list(self):
        defense_names = [name for name in self.defense_library.defenses.keys()]
        defense_names.sort()
        self.list_defenses.clear()

        for defense_name in defense_names:
            self.list_defenses.addItem(defense_name)

    def handle_defense_clicked(self, defense_clicked):
        defense_name = defense_clicked.data(0)
        self.edit_defense_name.setText(defense_name)
        self.modifying_defense.copy_from(self.defense_library.defenses[defense_name])

        self.cb_d1.setChecked(True if 'D1' in self.modifying_defense.affected_tags else False)
        self.cb_d2.setChecked(True if 'D2' in self.modifying_defense.affected_tags else False)
        self.cb_d3.setChecked(True if 'D3' in self.modifying_defense.affected_tags else False)
        self.cb_d4.setChecked(True if 'D4' in self.modifying_defense.affected_tags else False)
        self.cb_d5.setChecked(True if 'D5' in self.modifying_defense.affected_tags else False)
        self.cb_d6.setChecked(True if 'D6' in self.modifying_defense.affected_tags else False)
        self.cb_d7.setChecked(True if 'D7' in self.modifying_defense.affected_tags else False)
        self.cb_d8.setChecked(True if 'D8' in self.modifying_defense.affected_tags else False)
        self.cb_d9.setChecked(True if 'D9' in self.modifying_defense.affected_tags else False)
        self.cb_d10.setChecked(True if 'D10' in self.modifying_defense.affected_tags else False)
        self.cb_d11.setChecked(True if 'D11' in self.modifying_defense.affected_tags else False)

        self.combo_defender_to_edit.setCurrentIndex(0)
        self.handle_defender_change('D1')

    def handle_save_defense_library(self):
        with open('defense_library.json', 'w') as file:
            json.dump(self.defense_library.to_dict(), file, indent=3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DefensiveLibraryEditor()

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