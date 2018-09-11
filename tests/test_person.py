import unittest
import onexone.person

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.p = onexone.person.Person()

    def test__is_match_matches(self):
        self.assertTrue(self.p._is_match('banana', 'banana'))
        self.assertTrue(self.p._is_match('bananarama', 'banana'))

    def test__is_match_doesnt_match(self):
        self.assertFalse(self.p._is_match('banana', 'bananarama'))

    # TODO(mrda): Insert many more tests here
