import json


_ds = None


def get_datastore(filename="1x1-data"):
    global _ds
    if _ds is None:
        _ds = DataStore(filename)
    return _ds


class DataStore:

    def __init__(self, filename):
        self.ds = {}
        self.filename = filename
        self.load()

    def new_entry(self, name):
        self.ds[name] = None

    def list_entries(self):
        for key in sorted(self.ds.iterkeys()):
            print(key)

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
