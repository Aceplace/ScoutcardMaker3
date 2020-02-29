import sys
from qtgui import OffenseLibraryGUI, DefenseLibraryGUI, CompositeViewer, ExporterGUI

argument = sys.argv[1]

if argument == 'offensegui':
    OffenseLibraryGUI.launch()
elif argument == 'defensegui':
    DefenseLibraryGUI.launch()
elif argument == 'compositeviewer':
    CompositeViewer.launch()
elif argument == 'exportergui':
    ExporterGUI.launch()
