from os import path
import sys
sys.path.append(path.abspath(r"D:\OneDrive\Programming\ScoutCardMaker3\Core"))

import DefensiveConditionParser as parser

parser.parse('"Killer" and tenui(3, 5)')