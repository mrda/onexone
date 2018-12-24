import six.moves as sm
import sys
import unittest
import onexone.person

# Handle py2/3 and mock differences
if sys.version_info.major == 3:
    from unittest import mock
else:
    # Expect the `mock` package for python 2.
    # https://pypi.python.org/pypi/mock
    import mock


class TestMySanity(unittest.TestCase):

    @mock.patch('onexone.datastore.DataStore.save', create=True)
    @mock.patch('onexone.datastore.DataStore.load', create=True)
    def setUp(self, mock_load, mock_save):
        self.p = onexone.person.Person()
        _ = mock.ANY
        self.ds = onexone.datastore.get_datastore(_)
        self.ds.ds = {
                     'info': {
                             'version': _,
                             'name': _,
                             },
                     'people': {},
                     }

    # Person sanity tests
    @mock.patch('onexone.datastore.DataStore.save', create=True)
    @mock.patch('onexone.datastore.DataStore.load', create=True)
    def test_add_person(self, mock_load, mock_save):
        self.p.add(['Freddy', 'Nerks', 'Developer', 'True', '20170701',
                   '20180801'])
        freddy = self.ds.ds['people']['FreddyNerks']
        self.assertEqual('Freddy', freddy['meta']['first_name'])
        self.assertEqual('Nerks', freddy['meta']['last_name'])
        self.assertEqual('Developer', freddy['meta']['role'])
        self.assertTrue(freddy['meta']['enabled'])
        self.assertEqual('20170701', freddy['meta']['start_date'])
        self.assertEqual('20180801', freddy['meta']['end_date'])

    @mock.patch('six.moves.input', create=True)
    @mock.patch('onexone.datastore.DataStore.save', create=True)
    @mock.patch('onexone.datastore.DataStore.load', create=True)
    def test_delete_person(self, mock_load, mock_save, mock_input):
        mock_input.return_value = 'y'
        self.p.add(['Freddy', 'Nerks', 'Developer', 'True', '20170701',
                   '20180801'])
        self.assertTrue('FreddyNerks' in self.ds.ds['people'])
        self.p.delete(['Freddy', 'Nerks'])
        self.assertFalse('FreddyNerks' in self.ds.ds['people'])

    def test_list_person(self):
        # This function just prints things to the screen.
        # No sanity test provided
        pass

    @mock.patch('onexone.datastore.DataStore.save', create=True)
    @mock.patch('onexone.datastore.DataStore.load', create=True)
    def test_enable_person(self, mock_load, mock_save):
        self.p.add(['Freddy', 'Nerks', 'Developer', 'True', '20170701',
                   '20180801'])
        self.assertTrue(self.ds.ds['people']['FreddyNerks']['meta']['enabled'])
        self.p.enable(['Nerks', 'False'])
        self.assertFalse(self.ds.ds['people']['FreddyNerks']
                         ['meta']['enabled'])
        self.p.enable(['Nerks', 'True'])
        self.assertTrue(self.ds.ds['people']['FreddyNerks']['meta']['enabled'])

    def test_find_person(self):
        # This function just prints things to the screen.
        # No sanity test provided
        pass

    @mock.patch('onexone.person.Person._print_person', create=True)
    @mock.patch('onexone.datastore.DataStore.save', create=True)
    @mock.patch('onexone.datastore.DataStore.load', create=True)
    def test_info_person(self, mock_load, mock_save, mock_pp):
        # Important to reininitialise self.p so we can mock _print_person
        self.p = onexone.person.Person()
        self.p.add(['Freddy', 'Nerks', 'Developer', 'True', '20170701',
                   '20180801'])
        self.p.info(['Nerks'], False)
        mock_pp.assert_called_once_with('FreddyNerks')

    # TODO(mrda): Add sanity tests for meeting
    # TODO(mrda): Add sanity tests for help
    # TODO(mrda): Add sanity tests for version
