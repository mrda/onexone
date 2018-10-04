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

    def _add_meetings(self, fullname, meetings_list):
        self.ds.ds['people'][fullname]['meetings'] = meetings_list

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
        self._add_meetings('JohnCitizen', ['20181003'])

        self._make_person('JaneSmith', 'Jane', 'Smith', False)
        self._add_meetings('JaneSmith', ['20180907', '20181003'])

        self._make_person('CarlosSmith', 'Carlos', 'Smith', True)

        self._make_person('FredFlintstone', 'Fred', 'Flintstone', True)

    # Tests for version functions
    def test_version(self):
        self.assertEquals('9.3.6', self.ds.version())

    # Tests for list_fullnames
    def test_list_fullnames_enabled(self):
        self.assertItemsEqual(['JohnCitizen', 'CarlosSmith', 'FredFlintstone'],
                              self.ds.list_fullnames())

    def test_list_fullnames_disabled(self):
        self.assertItemsEqual(['JaneSmith'],
                              self.ds.list_fullnames(False))

    # Tests for list_everything
    def test_list_everything(self):
        fm = "{:>15} {:>15} {!s:>15} {:>15}"
        expected = fm.format('First Name', 'Last Name', 'Enabled?',
                             'Last OneOnOne') + '\n'
        expected += fm.format('Carlos', 'Smith', True, None) + '\n'
        expected += fm.format('Fred', 'Flintstone', True, None) + '\n'
        expected += fm.format('Jane', 'Smith', False, '20181003') + '\n'
        expected += fm.format('John', 'Citizen', True, '20181003') + '\n'
        self.assertEqual(expected, self.ds.list_everything())

    # Tests for find and _is_match
    def test__is_match_matches(self):
        self.assertTrue(self.ds._is_match('banana', 'banana'))
        self.assertTrue(self.ds._is_match('bananarama', 'banana'))

    def test__is_match_doesnt_match(self):
        self.assertFalse(self.ds._is_match('banana', 'bananarama'))

    # Tests for name functions
    def test_get_firstname_success(self):
        self.assertEquals('Carlos', self.ds.get_first_name('CarlosSmith'))

    def test_get_firstname_fail(self):
        self.assertEquals(None, self.ds.get_first_name('NonExistantPerson'))

    def test_get_lastname_success(self):
        self.assertEquals('Citizen', self.ds.get_last_name('JohnCitizen'))

    def test_get_firstname_fail(self):
        self.assertEquals(None, self.ds.get_last_name('NonExistantPerson'))

    # Tests for get_meetings
    def test_get_meetings_single_success(self):
        self.assertEquals(['20181003'],
                          self.ds.get_meetings('JohnCitizen'))

    def test_get_meetings_mutiple_success(self):
        self.assertItemsEqual(['20181003', '20180907'],
                              self.ds.get_meetings('JaneSmith'))

    def test_get_meetings_no_meetings_success(self):
        self.assertEquals([],
                          self.ds.get_meetings('FredFlintstone'))

    def test_get_meetings_no_such_person(self):
        self.assertEquals(None,
                          self.ds.get_meetings('NonExistantPerson'))

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
        self.assertItemsEqual(['JohnCitizen', 'CarlosSmith', 'FredFlintstone'],
                              self.ds.find('enabled', True))

    # Test for get_all_fullnames
    def test_get_all_fullnames(self):
        self.assertItemsEqual(['JaneSmith', 'CarlosSmith', 'FredFlintstone',
                              'JohnCitizen'],
                              self.ds.get_all_fullnames())

    # TODO(mrda): Tests for new_entry

    # TODO(mrda): Tests for remove_entry

    # TODO(mrda): Tests for save

    # TODO(mrda): Tests for load

    # TODO(mrda): Tests for add_meeting

    # TODO(mrda): Tests for delete_meeting
