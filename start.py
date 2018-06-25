import os
import sys
import time
from codecs import open

dirName = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirName + "\\Scripts")

# imports go HERE
from missingDivisionNamesGroup import missing_divisions_names_group
from checkForOldGenerals import check_for_old_generals
from checkForNameLists import check_for_name_lists
from checkBrackets import check_brackets
from checkForDoubleLocs import check_for_double_locs
from checkGFX import check_for_missing_gfx
from checkFocus import check_for_missing_focus
from checkCores import check_for_missing_cores
from checkEquipmentBonus import check_equipment_bonus
from checkIdeologies import check_ideologies
from checkEvents import check_events

# output file initialisation

# functions go HERE

def start(mod_path, hoi4_path):
    t0 = time.time()
    output_file = open("validator.txt", 'w', 'utf-8-sig')
    missing_divisions_names_group(mod_path, output_file)
    check_for_old_generals(mod_path, output_file)
    check_for_name_lists(mod_path, output_file)
    check_brackets(mod_path, output_file)
    check_for_double_locs(mod_path, output_file)
    #check_for_missing_gfx(mod_path, output_file, hoi4_path)
    check_for_missing_focus(mod_path, output_file)
    check_for_missing_cores(mod_path, output_file)
    check_equipment_bonus(mod_path, output_file)
    check_ideologies(mod_path, output_file)
    check_events(mod_path, output_file)
    t0 = time.time() - t0
    print("Total time taken: " + (t0*1000).__str__() + " ms")











