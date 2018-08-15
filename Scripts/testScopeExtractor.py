import unittest

from Scripts.scopeExtractor import ScopeExtractor


class TestScopeExtractorByType(unittest.TestCase):

    def setUp(self):
        scope = 'scope'
        self.scope_extractor = ScopeExtractor(scope)

    def test_single_line_body(self):
        expected_body = 'scope = { field = contents field = contents }'

        gen = self.scope_extractor.get_next_scope(expected_body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_single_line_index(self):
        body = 'scope = { field = contents field = contents }'
        expected_index = 1

        gen = self.scope_extractor.get_next_scope(body)
        actual_index, extracted_body = next(gen)

        self.assertEqual(expected_index, actual_index)

    def test_no_optional_spaces(self):
        expected_body = 'scope={field=contents field=contents}'

        gen = self.scope_extractor.get_next_scope(expected_body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_multiline_body(self):
        expected_body = 'scope = {\n field = contents\n field = contents\n }'

        gen = self.scope_extractor.get_next_scope(expected_body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_nested_scope(self):
        expected_body = 'scope = {\n field = {\n subfield = contents\n}\n}'

        gen = self.scope_extractor.get_next_scope(expected_body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_remove_leading_lines(self):
        body = 'other_line\nscope = {\n field = contents\n field = contents\n }'
        expected_body = 'scope = {\n field = contents\n field = contents\n }'

        gen = self.scope_extractor.get_next_scope(body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_remove_trailing_lines(self):
        body = 'scope = {\n field = contents\n field = contents\n }\nother_line'
        expected_body = 'scope = {\n field = contents\n field = contents\n }'

        gen = self.scope_extractor.get_next_scope(body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_multiple_on_line(self):
        body = 'field = contents scope = contents field = contents'
        expected_body = 'scope = contents'

        gen = self.scope_extractor.get_next_scope(body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)

    def test_trailing_endline(self):
        body = 'scope = contents\n'
        expected_body = 'scope = contents'

        gen = self.scope_extractor.get_next_scope(body)
        index, actual_body = next(gen)

        self.assertEqual(expected_body, actual_body)


if __name__ == '__main__':
    unittest.main()
