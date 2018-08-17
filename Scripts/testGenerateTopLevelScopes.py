import unittest

from Scripts.generateScopes import generate_scopes
from Scripts.generateTopLevelScopeIndices import generate_top_level_scope_indices


class TestScopeExtractorByType(unittest.TestCase):

    def test_single_line(self):
        body = 'scope = { field = contents field = contents }'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        actual = next(gen)

        expected = (1, 'scope', 'field = contents field = contents')
        self.assertEqual(expected, actual)

    def test_no_optional_spaces(self):
        body = 'scope={field=contents field=contents}'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        actual = next(gen)

        expected = (1, 'scope', 'field=contents field=contents')
        self.assertEqual(expected, actual)

    def test_multiline_body(self):
        body = 'scope = {\n field = contents\n field = contents\n }'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        actual = next(gen)

        expected = (1, 'scope', 'field = contents\n field = contents')
        self.assertEqual(expected, actual)

    def test_multiple_layers_in_body(self):
        body = 'scope = {\n field = {\n subfield = contents\n}\n}'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        actual = next(gen)

        expected = (1, 'scope', 'field = {\n subfield = contents\n}')
        self.assertEqual(expected, actual)

    def test_remove_leading_lines(self):
        body = 'other_line\nscope = {\n field = contents\n field = contents\n }'
        expected_body = 'field = contents\n field = contents'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        index, name, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_remove_trailing_lines(self):
        body = 'scope = {\n field = contents\n field = contents\n }\nother_line'
        expected_body = 'field = contents\n field = contents'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        index, name, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_multiple_on_line(self):
        body = 'field = contents scope = contents field = contents'
        expected_body = 'contents'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        next(gen)

        index, name, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_trailing_endline(self):
        body = 'scope = contents\n'
        expected_body = 'contents'

        gen = generate_scopes(body, generate_top_level_scope_indices)
        index, name, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)


if __name__ == '__main__':
    unittest.main()
