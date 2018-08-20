import json


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
