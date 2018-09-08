import debugging
import json

_ds = None


debug = False
debugging._debug = debug


@debugging.trace
def get_datastore(filename="1x1-data"):
    global _ds
    if _ds is None:
        _ds = DataStore(filename)
    return _ds


def choose_location(filename):
    ds = get_datastore(filename)


class DataStore:

    _all_format = "{:>15} {:>15} {:>15} {:>15}"

    def __init__(self, filename):
        self.ds = {}
        self.filename = filename
        self.load()

    def new_entry(self, key, value=None):
        self.ds[key] = value

    def list_keys(self):
        for key in sorted(self.ds.iterkeys()):
            print(key)

    @debugging.trace
    def list_everything(self):
        print(DataStore._all_format.format(
              "First Name", "Last Name", "Enabled?", "Last 1x1"))
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
