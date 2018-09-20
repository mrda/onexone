import unittest
import onexone.datastore

class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.ds = onexone.datastore.get_datastore()
        self.ds._ds_version['major'] = 9
        self.ds._ds_version['minor'] = 6
        self.ds._ds_version['patch'] = 3

    def test_version(self):
        self.assertEquals('9.6.3', self.ds.version())

    def test_major_version(self):
        self.assertEquals(9, self.ds.major_version())

    def test_minor_version(self):
        self.assertEquals(6, self.ds.minor_version())
