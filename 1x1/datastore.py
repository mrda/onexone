import json

_ds = None


def get_datastore(filename="1x1-data"):
    global _ds
    if _ds is None:
        _ds = DataStore(filename)
    return _ds


def choose_location(filename):
    ds = get_datastore(filename)


class DataStore:

    def __init__(self, filename):
        self.ds = {}
        self.filename = filename
        self.load()

    def new_entry(self, key, value=None):
        self.ds[key] = value

    def list_keys(self):
        for key in sorted(self.ds.iterkeys()):
            print(key)

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
