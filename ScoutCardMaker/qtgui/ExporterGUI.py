import os

from qtgui.UI_Exporter import Ui_ExportGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QPushButton, QVBoxLayout
import sys
import json
from scoutcardmaker.Offense import OffenseLibrary
from scoutcardmaker.Defense import DefenseLibrary
from scriptexports.excelscriptparser import get_script_from_excel_file
from scriptexports.powerpointexporter import export_to_powerpoint, export_to_powerpoint_alternating
from scriptexports.footballtrainerscriptexport import export_to_football_trainer


class ExportGUI(QMainWindow, Ui_ExportGui):
    def __init__(self, last_load_location, last_save_location, update_directory_location_callback):
        super().__init__()
        self.setupUi(self)
        self.last_load_location = last_load_location
        self.last_save_location = last_save_location
        self.formation_library = OffenseLibrary()
        self.defense_libary = DefenseLibrary()
        self.update_directory_location_callback = update_directory_location_callback
        self.actionCreate_Scout_Cards.triggered.connect(lambda: self.handle_create_scout_cards(False, False))
        self.actionCreate_Scout_Cards_Alternating.triggered.connect(lambda: self.handle_create_scout_cards(True, False))
        self.action_Off_Create_Scout_Cards.triggered.connect(lambda: self.handle_create_scout_cards(False, True))
        self.action_Off_Create_Scout_Cards_Alternating.triggered.connect(lambda: self.handle_create_scout_cards(True, True))
        self.actionCreate_Football_Trainer_Script.triggered.connect(self.handle_create_football_trainer_script)
        self.cb_college_hash_marks.stateChanged.connect(self.handle_cb_college_hash_marks_changed)
        self.show()

    def load_offense_library_from_dict(self, library_dict):
        self.formation_library = OffenseLibrary.from_dict(library_dict)

    def load_defense_library_from_dict(self, library_dict):
        self.defense_library = DefenseLibrary.from_dict(library_dict)

    def handle_create_scout_cards(self, alternating, offense):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Choose Script', self.last_load_location, 'Excel File (*.xlsx)')
            if not file_name:
                return

            self.last_load_location = os.path.dirname(file_name) + '/'
            success, script = get_script_from_excel_file(file_name, self.get_sheet_choice_callback)

            file_name, _ = QFileDialog.getSaveFileName(self, 'Scout Card Filename', self.last_save_location, 'Power Point (*.pptx)')
            if not file_name:
                return

            self.last_save_location = os.path.dirname(file_name) + '/'
            if alternating:
                export_to_powerpoint_alternating(file_name, script, self.formation_library, self.defense_library, offense, self.cb_college_hash_marks.isChecked())
            else:
                export_to_powerpoint(file_name, script, self.formation_library, self.defense_library, offense, self.cb_college_hash_marks.isChecked())

            self.update_directory_location_callback(self.last_load_location, self.last_save_location)

        except Exception:
            import traceback
            traceback.print_exc()

    def handle_create_football_trainer_script(self, alternating):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Choose Script', self.last_load_location, 'Excel File (*.xlsx)')
            if not file_name:
                return

            self.last_load_location = os.path.dirname(file_name) + '/'
            success, script = get_script_from_excel_file(file_name, self.get_sheet_choice_callback)

            file_name, _ = QFileDialog.getSaveFileName(self, 'Trainer Script', self.last_save_location, 'JSON (*.json)')
            if not file_name:
                return

            self.last_save_location = os.path.dirname(file_name) + '/'
            export_to_football_trainer(file_name, script, self.formation_library, self.defense_library)

            self.update_directory_location_callback(self.last_load_location, self.last_save_location)

        except Exception:
            import traceback
            traceback.print_exc()

    def handle_cb_college_hash_marks_changed(self):
        with open('hash_mark_preferences.txt', 'w') as file:
            file.write('college' if self.cb_college_hash_marks.isChecked() else 'high_school')

    def get_sheet_choice_callback(self, choices):
        choose_sheet_dialog = ChooseSheetDialog(choices)
        choose_sheet_dialog.chosen_sheet
        choose_sheet_dialog.exec_()
        return choose_sheet_dialog.chosen_sheet


class ChooseSheetDialog(QDialog):
    def __init__(self, choices):
        super(ChooseSheetDialog, self).__init__()

        self.setWindowTitle("Choose Sheet")
        self.chosen_sheet = None

        vbox = QVBoxLayout()
        for choice in choices:
            btn = QPushButton(self)
            btn.setText(choice)
            btn.clicked.connect(lambda ignore, choice=choice: self.handle_choice(choice))
            vbox.addWidget(btn)

        self.setLayout(vbox)

    def handle_choice(self, choice):
        self.chosen_sheet = choice
        self.accept()


def launch(last_load_location, last_save_location, update_last_directory_callback):
    app = QApplication(sys.argv)
    window = ExportGUI(last_load_location, last_save_location, update_last_directory_callback)
    window.setWindowTitle('Script Exporter')

    try:
        with open('offense_library.json', 'r') as file:
            window.load_offense_library_from_dict(json.load(file))
    except FileNotFoundError:
        print('Offensive library file not found')

    try:
        with open('defense_library.json', 'r') as file:
            window.load_defense_library_from_dict(json.load(file))
    except FileNotFoundError:
        print('Defensive library file not found')

    try:
        with open('hash_mark_preferences.txt') as file:
            preference = file.readline()
            window.cb_college_hash_marks.setChecked(True if preference == 'college' else False)
    except FileNotFoundError:
        print('Hash mark preference not found')

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()