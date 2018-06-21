import time
from Scripts.scopeScanner import ScopeScanner


def check_equipment_bonus(path, output_file):
    t0 = time.time()

    subpaths = ['\\common\\ideas']
    scope = 'equipment_bonus'

    equipment_bonus_checker = EquipmentBonusChecker(path, subpaths, scope=scope)
    equipment_bonuses = equipment_bonus_checker.scan_files()

    for equipment_bonus in equipment_bonuses:
        output_file.write("\'instant = yes\' missing from equipment_bonus scope ending at " + str(
            equipment_bonus.line) + ' in ' + equipment_bonus.filename + '\n')

    t0 = time.time() - t0
    print("Time taken for equipment bonus script: " + (t0*1000).__str__() + " ms")


class EquipmentBonus:

    def __init__(self, line_number, filename):
        self.line = line_number
        self.filename = filename


class EquipmentBonusChecker(ScopeScanner):

    def initialize_additional_variables(self):
        self.equipment_bonuses = []

    def actions_on_scope_start(self):
        pass

    def actions_in_scope(self):
        if self.scope_level == 1:
            equipment = self.line.strip(' \t\n\r').split(' ')[0]
            if (equipment != '') & (equipment != '}'):
                if 'instant' in self.line:
                    self.instant_found = True
                else:
                    self.instant_found = False
        elif self.scope_level == 2:
            if 'instant' in self.line:
                self.instant_found = True

    def actions_on_scope_level_change(self, change):
        if (self.scope_level == 2) & (change == -1):
            if not self.instant_found:
                flagged_equipment_bonus = EquipmentBonus(self.current_line, self.filename)
                self.equipment_bonuses += [flagged_equipment_bonus]

    def return_outputs(self):
        return self.equipment_bonuses