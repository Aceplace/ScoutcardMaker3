import sys
from qtgui import OffenseLibraryGUI, DefenseLibraryGUI, CompositeViewer, ExporterGUI

argument = sys.argv[1]

with open('last_directory_locations.txt', 'r') as file:
    last_load_location = file.readline()
    last_save_location = file.readline()

def new_last_directory_callback(last_load_location, last_save_location):
    with open('last_directory_locations.txt', 'w') as file:
        file.writelines((last_load_location, '\n', last_save_location))

if argument == 'offensegui':
    OffenseLibraryGUI.launch()
elif argument == 'defensegui':
    DefenseLibraryGUI.launch()
elif argument == 'compositeviewer':
    CompositeViewer.launch()
elif argument == 'exportergui':
    ExporterGUI.launch(last_load_location, last_save_location, new_last_directory_callback)
