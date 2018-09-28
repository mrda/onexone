import debugging
import json

_ds = None


debug = False
debugging._debug = debug


@debugging.trace
def get_datastore(filename="onexone-data"):
    global _ds
    if _ds is None:
        _ds = DataStore(filename)
    return _ds


def choose_location(filename):
    ds = get_datastore(filename)


class DataStore:

    # Note(mrda): Need to force booleans to be displayed as strings, so that
    # 'True' is printed instead of '1'.
    _all_format = "{:>15} {:>15} {!s:>15} {:>15}"

    _ds_version = {
        'major': 1,
        'minor': 0,
        'patch': 0,
    }

    def __init__(self, filename):
        self.ds = {}
        self.filename = filename
        self.load()

    def new_entry(self, key, value=None):
        self.ds[key] = value

    def remove_entry(self, key):
        # Note(mrda): No error if key isn't in dict
        self.ds.pop(key, None)

    def version(self):
        return "{}.{}.{}".format(DataStore._ds_version['major'],
                                 DataStore._ds_version['minor'],
                                 DataStore._ds_version['patch'])

    def major_version(self):
        return DataStore._ds_version['major']

    def minor_version(self):
        return DataStore._ds_version['minor']

    def list_keys(self, enabled=True):
        for key in sorted(self.ds.iterkeys()):
            if self.ds[key]['meta']['enabled'] == enabled:
                print(key)

    @debugging.trace
    def list_everything(self):
        print(DataStore._all_format.format(
              "First Name", "Last Name", "Enabled?", "Last OneOnOne"))
        for key in sorted(self.ds.iterkeys()):
            meetings = sorted(self.ds[key]['meetings'], reverse=True)
            latest_meeting = None
            if meetings:
                latest_meeting = meetings[0]
            print(DataStore._all_format.format(
                  self.ds[key]['meta']['first_name'],
                  self.ds[key]['meta']['last_name'],
                  self.ds[key]['meta']['enabled'],
                  latest_meeting))

    def get_dict(self):
        return self.ds

    def get_value(self, key):
        return self.ds[key]

    def set_enabled(self, fullname, enabled):
        self.ds[fullname]['meta']['enabled'] = enabled
        self.save()

    def get_all_fullnames(self):
        """Return all fullnames as a list."""
        return list(self.ds.keys())

    def get_meetings(self, key):
        return self.ds[key]['meetings']

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.ds, f)

    def load(self):
        try:
            with open(self.filename, "r") as f:
                self.ds = json.load(f)
        except IOError:
            self.ds = {}

    def dump(self):
        print("Dumping data")
        print self.ds
