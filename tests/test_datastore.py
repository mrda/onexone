import unittest
import onexone.datastore

class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.ds = onexone.datastore.get_datastore()
        self.ds._ds_version['major'] = 9
        self.ds._ds_version['minor'] = 6
        self.ds._ds_version['patch'] = 3

    # TODO(mrda): Tests for new_entry

    # TODO(mrda): Tests for remove_entry

    # TODO(mrda): Tests for version functions

    def test_version(self):
        self.assertEquals('9.6.3', self.ds.version())

    def test_major_version(self):
        self.assertEquals(9, self.ds.major_version())

    def test_minor_version(self):
        self.assertEquals(6, self.ds.minor_version())

    # TODO(mrda): Tests for list_keys

    # TODO(mrda): Tests for list_everything

    # TODO(mrda): Tests for get_dict

    # TODO(mrda): Tests for get_value

    # TODO(mrda): Tests for set_enabled

    # TODO(mrda): Tests for get_all_fullnames

    # TODO(mrda): Tests for get_meetings

    # TODO(mrda): Tests for save

    # TODO(mrda): Tests for load

    # TODO(mrda): Tests for dump
