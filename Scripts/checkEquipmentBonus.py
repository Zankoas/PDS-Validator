from os import listdir
import time
from openFile import open_file


def check_equipment_bonus(path, output_file):
    t0 = time.time()
    subpath = path + '\\common\\ideas'

    for filename in listdir(subpath):
        current_line = 1

        file = open_file(subpath + '\\' + filename)
        line = file.readline()

        while line:
            if "equipment_bonus" in line:
                in_equipment_bonus_scope = True
                instant_equals_yes_found = False
                scope_level = 1
                line = file.readline()
                current_line += 1

                while in_equipment_bonus_scope & bool(line):
                    if instant_equals_yes_found == False:
                        instant_equals_yes_found = check_for_instant_equals_yes(line)
                    scope_level += change_in_scope_level(line)
                    if scope_level == 0:
                        in_equipment_bonus_scope = False
                        if not instant_equals_yes_found:
                            output_file.write("\'instant = yes\' missing from equipment_bonus scope ending at " + str(current_line) + ' in ' + filename + '\n')
                    line = file.readline()
                    current_line += 1
            else:
                line = file.readline()
                current_line += 1


    t0 = time.time() - t0
    print("Time taken for equipment bonus script: " + (t0*1000).__str__() + " ms")


def check_for_instant_equals_yes(line):
    instant_equals_yes_found = False
    for string in ['instant = yes', 'instant=yes', 'instant =yes', 'instant= yes']:
        if string in line:
            instant_equals_yes_found = True
    return instant_equals_yes_found


def change_in_scope_level(line):
    change = 0
    for character in line:
        if character == '{':
            change += 1
        elif character == '}':
            change += -1
    return change
