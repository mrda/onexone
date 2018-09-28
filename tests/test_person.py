import unittest
import onexone.person

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.p = onexone.person.Person()

    # TODO(mrda): Tests for _is_match

    def test__is_match_matches(self):
        self.assertTrue(self.p._is_match('banana', 'banana'))
        self.assertTrue(self.p._is_match('bananarama', 'banana'))

    def test__is_match_doesnt_match(self):
        self.assertFalse(self.p._is_match('banana', 'bananarama'))

    # TODO(mrda): Tests for _search

    # TODO(mrda): Tests for _find

    # TODO(mrda): Tests for find_person

    # TODO(mrda): Tests for _exact_match

    # TODO(mrda): Tests for find

    # TODO(mrda): Tests for is_anabled

    # TODO(mrda): Tests for info

    # TODO(mrda): Tests for _print_person

    # TODO(mrda): Tests for _build_filename

    # TODO(mrda): Tests for _new_person

    # TODO(mrda): Tests for add

    # TODO(mrda): Tests for delete

    # TODO(mrda): Tests for info

    # TODO(mrda): Tests for list

    # TODO(mrda): Tests for enable

    # TODO(mrda): Tests for parse
