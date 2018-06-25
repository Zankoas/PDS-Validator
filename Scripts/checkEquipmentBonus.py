import time
from Scripts.getAllFilenames import get_all_filenames
from Scripts.scopeExtractor import ScopeExtractorByType, ScopeExtractorByScopeLevel


def check_equipment_bonus(path, output_file):
    t0 = time.time()

    equipment_bonus_scopes = find_equipment_bonus_scopes(path)
    equipment_bonuses = find_equipment_bonuses(equipment_bonus_scopes)
    flagged_equipment_bonuses = validate_equipment_bonuses(equipment_bonuses)

    for equipment_bonus in flagged_equipment_bonuses:
        output_file.write("\'instant \' field missing from equipment bonus starting at " + str(
            equipment_bonus.starting_line) + ' in ' + equipment_bonus.filename + '\n')

    t0 = time.time() - t0
    print("Time taken for equipment bonus script: " + (t0*1000).__str__() + " ms")


def find_equipment_bonuses(equipment_bonus_scopes):
    equipment_bonuses = []
    for equipment_bonus_scope in equipment_bonus_scopes:
        eq_bonus_extractor = ScopeExtractorByScopeLevel(1)
        equipment_bonuses_in_this_scope = eq_bonus_extractor.from_string(equipment_bonus_scope.body, equipment_bonus_scope.filename)
        for equipment_bonus in equipment_bonuses_in_this_scope:
            equipment_bonus.starting_line += equipment_bonus_scope.starting_line - 1
        equipment_bonuses += equipment_bonuses_in_this_scope
    return equipment_bonuses


def validate_equipment_bonuses(equipment_bonuses):
    flagged_equipment_bonuses = []
    for equipment_bonus in equipment_bonuses:
        if 'instant' not in equipment_bonus.body:
            flagged_equipment_bonuses += [equipment_bonus]
    return flagged_equipment_bonuses


def find_equipment_bonus_scopes(path):
    subpath = '\\common\\ideas'
    scope_type = 'equipment_bonus'
    full_path = path + subpath

    eq_bonus_scope_extractor = ScopeExtractorByType(scope_type)
    equipment_bonuses = eq_bonus_scope_extractor.from_path(full_path)
    return equipment_bonuses
