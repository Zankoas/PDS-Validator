import time
from Scripts.fileScanner import FileScanner
from Scripts.scopeExtractor import ScopeExtractorByType, ScopeExtractorByScopeLevel
from Scripts.getAllFilenames import get_all_filenames


def check_ideologies(path, output_file):
    t0 = time.time()

    ideology_references = find_references_to_ideologies(path)
    ideology_scopes = find_ideology_scopes(path)
    ideologies = find_ideologies(ideology_scopes)
    ideology_names = find_ideology_names(ideologies)
    references_needing_ideology = check_if_reference_names_present_in_ideology_names(ideology_references, ideology_names)

    for reference in references_needing_ideology:
        output_file.write("Ideology " + reference.body + " not defined at " + str(reference.starting_line)
                          + ' in ' + reference.filename + '\n')

    t0 = time.time() - t0
    print("Time taken for ideology reference script: " + (t0*1000).__str__() + " ms")


def find_ideology_names(ideologies):
    ideology_names = []
    for ideology in ideologies:
        body = ideology.body.strip(' \n\t\r')
        words = body.split(' ')
        ideology_names += [words[0]]
    return ideology_names


def check_if_reference_names_present_in_ideology_names(ideology_references, ideology_names):
    references_needing_ideology = []
    for reference in ideology_references:
        ideology_defined = False
        for ideology_name in ideology_names:
            if ideology_name == reference.body:
                ideology_defined = True
        if not ideology_defined:
            references_needing_ideology += [reference]
    return references_needing_ideology


def find_references_to_ideologies(path):
    subpaths = ['\\common', '\\events', '\\history']
    scope = 'has_government'
    ideology_references = []
    for subpath in subpaths:
        ideology_reference_finder = IdeologyReferenceFinder(scope)
        ideology_references += ideology_reference_finder.from_path(path+subpath)
    for reference in ideology_references:
        body_after_has_government = reference.body[reference.body.index('has_government') + 17:]
        reference_name = body_after_has_government.split(' ')[0].strip('\n\t\r}')
        reference.body = reference_name
    return ideology_references


def find_ideologies(ideology_scopes):
    ideologies = []
    ideology_extractor = ScopeExtractorByScopeLevel(1)
    for ideology_scope in ideology_scopes:
        ideologies_in_this_scope = ideology_extractor.from_string(ideology_scope.body, ideology_scope.filename)
        for ideology in ideologies_in_this_scope:
            ideology.starting_line += ideology_scope.starting_line - 1
        ideologies += ideologies_in_this_scope
    return ideologies


def find_ideology_scopes(path):
    subpath = '\\common\\ideologies'
    scope = 'ideologies'
    full_path = path + subpath

    ideology_scope_finder = ScopeExtractorByType(scope)
    ideology_scopes = ideology_scope_finder.from_path(full_path)
    return ideology_scopes


class IdeologyReferenceFinder(ScopeExtractorByType):

    def _extract_scope_body(self):
        return self.line