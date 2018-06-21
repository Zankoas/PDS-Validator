import time
from Scripts.fileScanner import FileScanner
from Scripts.scopeScanner import ScopeScanner


def check_ideologies(path, output_file):
    t0 = time.time()

    ideology_references = find_references_to_ideologies(path)
    ideologies = find_ideologies(path)
    references_needing_ideology = check_if_reference_names_present_in_ideology_names(ideology_references, ideologies)

    for reference in references_needing_ideology:
        output_file.write("Ideology " + reference.name + " not defined at " + str(reference.line_number)
                          + ' in ' + reference.filename + '\n')

    t0 = time.time() - t0
    print("Time taken for ideology reference script: " + (t0*1000).__str__() + " ms")


def check_if_reference_names_present_in_ideology_names(ideology_references, ideologies):
    references_needing_ideology = []
    for reference in ideology_references:
        ideology_defined = False
        for ideology in ideologies:
            if ideology == reference.name:
                ideology_defined = True
        if not ideology_defined:
            references_needing_ideology += [reference]
    return references_needing_ideology


def find_references_to_ideologies(path):
    subpaths = ['\\common', '\\events', '\\history']

    ideology_reference_finder = IdeologyReferenceFinder(path, subpaths)
    return ideology_reference_finder.scan_files()


def find_ideologies(path):
    subpath = ['\\common\\ideologies']
    scope = 'ideologies'

    ideology_finder = IdeologyFinder(path, subpath, scope=scope)
    return ideology_finder.scan_files()


class IdeologyFinder(ScopeScanner):

    def initialize_additional_variables(self):
        self.ideologies = []

    def actions_in_scope(self):
        ideology_name = self.line.strip(' \t\n\r').split(' ')[0]
        if (ideology_name != '') & (ideology_name != '}'):
            self.ideologies += [ideology_name]

    def return_outputs(self):
        return self.ideologies


class IdeologyReferenceFinder(FileScanner):

    def initialize_additional_variables(self):
        self.ideology_references = []

    def while_in_file(self):
        if 'has_government' in self.line:
            words = self.line.split(' ')
            ideology_name = words[len(words) - 1]
            ideology_name = ideology_name.strip(' \n\t\r')
            if (ideology_name != '') & (ideology_name != '}'):
                ideology_reference = IdeologyReference(ideology_name, self.filename, self.current_line)
                self.ideology_references += [ideology_reference]

    def return_outputs(self):
        return self.ideology_references


class IdeologyReference:

    def __init__(self, name, filename, line_number):
        self.name = name
        self.filename = filename
        self.line_number = line_number
