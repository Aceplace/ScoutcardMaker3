from qtgui.UI_Exporter import Ui_ExportGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QPushButton, QVBoxLayout
import sys
import json
from scoutcardmaker.Offense import OffenseLibrary
from scoutcardmaker.Defense import DefenseLibrary
from scriptexports.excelscriptparser import get_script_from_excel_file


class ExportGUI(QMainWindow, Ui_ExportGui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formation_library = OffenseLibrary()
        self.defense_libary = DefenseLibrary()
        self.actionCreate_Scout_Cards.triggered.connect(self.handle_create_scout_cards)

        self.show()

    def load_offense_library_from_dict(self, library_dict):
        self.formation_library = OffenseLibrary.from_dict(library_dict)

    def load_defense_library_from_dict(self, library_dict):
        self.defense_library = DefenseLibrary.from_dict(library_dict)

    def handle_create_scout_cards(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Choose Script', 'c:\\', 'Excel File (*.xlsx)')
            print(file_name)
            if file_name:
                script = get_script_from_excel_file(file_name, self.get_sheet_choice_callback)
                print(script)
        except Exception:
            import traceback
            traceback.print_exc()

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
            print(choice)
            btn.clicked.connect(lambda ignore, choice=choice: self.handle_choice(choice))
            vbox.addWidget(btn)

        self.setLayout(vbox)

    def handle_choice(self, choice):
        self.chosen_sheet = choice
        self.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExportGUI()

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

    sys.exit(app.exec_())