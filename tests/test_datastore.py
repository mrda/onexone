import mock
import unittest

import onexone.datastore

class TestDataStore(unittest.TestCase):


    def _make_person(self, fullname, firstname, lastname, enabled):
        # Test helper function
        person = {
                 'meta': {
                         'first_name': firstname,
                         'last_name': lastname,
                         'enabled': enabled,
                         },
                 'meetings': [],
                 }
        self.ds.ds['people'][fullname] = person

    @mock.patch('onexone.datastore.DataStore.load', create=True)
    def setUp(self, mock_load):
        fn = 'fred'
        self.ds = onexone.datastore.get_datastore(fn)
        self.ds.ds = {
                     'info': {
                             'version' : '9.3.6',
                             'name' : fn,
                             },
                     'people': {},
                     }
        self._make_person('JohnCitizen', 'John', 'Citizen', True)
        self._make_person('JaneSmith', 'Jane', 'Smith', False)
        self._make_person('CarlosSmith', 'Carlos', 'Smith', True)

    # TODO(mrda): Tests for new_entry

    # TODO(mrda): Tests for remove_entry

    # Tests for version functions
    def test_version(self):
        self.assertEquals('9.3.6', self.ds.version())

    # Tests for list_keys
    def test_list_fullnames_enabled(self):
        self.assertItemsEqual(['JohnCitizen', 'CarlosSmith'],
                              self.ds.list_fullnames())

    def test_list_fullnames_disabled(self):
        self.assertItemsEqual(['JaneSmith'],
                              self.ds.list_fullnames(False))

    # TODO(mrda): Tests for list_everything

    # TODO(mrda): Tests for find and _is_match
    def test__is_match_matches(self):
        self.assertTrue(self.ds._is_match('banana', 'banana'))
        self.assertTrue(self.ds._is_match('bananarama', 'banana'))

    def test__is_match_doesnt_match(self):
        self.assertFalse(self.ds._is_match('banana', 'bananarama'))

    # TODO(mrda): Tests for get_dict
    # Note(mrda): get_dict should be removed

    # TODO(mrda): Tests for get_value

    # Tests for person enabled functions
    def test_is_enabled(self):
        self.assertTrue(self.ds.is_enabled('JohnCitizen'))

    def test_is_enabled_false(self):
        self.assertFalse(self.ds.is_enabled('JaneSmith'))

    def test_is_enabled_exception(self):
        self.assertRaises(KeyError, self.ds.is_enabled, 'RupertHumperdink')

    @mock.patch('onexone.datastore.DataStore.save', create=True)
    def test_set_enabled(self, mock_save):
        self.assertFalse(self.ds.is_enabled('JaneSmith'))
        self.ds.set_enabled('JaneSmith')
        mock_save.called_once()
        self.assertTrue(self.ds.is_enabled('JaneSmith'))
        self.ds.set_enabled('JaneSmith', False)
        self.assertFalse(self.ds.is_enabled('JaneSmith'))

    def test_find_match_single(self):
        self.assertEqual(['JohnCitizen'], self.ds.find('first_name', 'John'))

    def test_find_match_nomatch(self):
        self.assertEqual(None, self.ds.find('first_name', 'Rupert'))

    def test_find_match_multiple(self):
        self.assertItemsEqual(['JaneSmith', 'CarlosSmith'],
                              self.ds.find('last_name', 'Smith'))

    def test_find_match_enabled_false(self):
        self.assertEqual(['JaneSmith'], self.ds.find('enabled', False))

    def test_find_match_enabled_true(self):
        self.assertItemsEqual(['JohnCitizen', 'CarlosSmith'],
                              self.ds.find('enabled', True))

    # TODO(mrda): Tests for get_all_fullnames

    # TODO(mrda): Tests for get_meetings

    # TODO(mrda): Tests for save

    # TODO(mrda): Tests for load

    # TODO(mrda): Tests for dump
