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

    _PEOPLE = 'people'
    _META = 'meta'
    _INFO = 'info'
    _FIRST = 'first_name'
    _LAST = 'last_name'
    _MEETINGS = 'meetings'
    _ENABLED = 'enabled'
    _FILENAME = 'filename'
    _VERSION = 'version'

    # Note(mrda): Need to force booleans to be displayed as strings, so that
    # 'True' is printed instead of '1'.
    _all_format = "{:>15} {:>15} {!s:>15} {:>15}"

    _empty_store = {
                   _INFO: {
                       _VERSION: '',
                       _FILENAME: '',
                          },
                   _PEOPLE: {},
                   }

    _ds_version = {
        'major': 1,
        'minor': 0,
        'patch': 0,
    }

    def __init__(self, filename):
        self.ds = {}
        self.filename = filename
        self.load(self.filename)

    # notested
    def new_entry(self, key, value=None):
        self.ds[self._PEOPLE][key] = value

    # notested
    def remove_entry(self, key):
        # Note(mrda): No error if key isn't in dict
        self.ds[self._PEOPLE].pop(key, None)

    # notested
    def _make_version(self):
        return "{}.{}.{}".format(DataStore._ds_version['major'],
                                 DataStore._ds_version['minor'],
                                 DataStore._ds_version['patch'])

    # notested
    def _set_info(self):
        self.ds[self._INFO][self._VERSION] = self._make_version()
        self.ds[self._INFO][self._FILENAME] = self.filename

    def version(self):
        return self.ds[self._INFO][self._VERSION]

    # notested
    def list_fullnames(self, enabled=True):
        keys = set()
        for key in sorted(self.ds[self._PEOPLE].iterkeys()):
            if self.ds[self._PEOPLE][key][self._META][self._ENABLED] == \
               enabled:
                keys.add(key)

        if len(keys) == 0:
            return None

        return keys

    # notested
    @debugging.trace
    def list_everything(self):
        print(DataStore._all_format.format(
              "First Name", "Last Name", "Enabled?", "Last OneOnOne"))
        for key in sorted(self.ds[self._PEOPLE].iterkeys()):
            meetings = sorted(self.ds[self._PEOPLE][key][self._MEETINGS],
                              reverse=True)
            latest_meeting = None
            if meetings:
                latest_meeting = meetings[0]
            print(DataStore._all_format.format(
                  self.ds[self._PEOPLE][key][self._META][self._FIRST],
                  self.ds[self._PEOPLE][key][self._META][self._LAST],
                  self.ds[self._PEOPLE][key][self._META][self._ENABLED],
                  latest_meeting))

    # notested
    def get_value(self, key):
        return self.ds[key]

    def is_enabled(self, fullname):
        return self.ds[self._PEOPLE][fullname][self._META][self._ENABLED]

    def set_enabled(self, fullname, enabled=True):
        self.ds[self._PEOPLE][fullname][self._META][self._ENABLED] = enabled
        self.save()

    # notested
    def get_all_fullnames(self):
        """Return all fullnames as a list."""
        return list(self.ds.keys())

    # notested
    def get_meetings(self, key):
        return self.ds[key][self._MEETINGS]

    # notested
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.ds, f)

    # notested
    def load(self, filename):
        try:
            with open(filename, "r") as f:
                self.ds = json.load(f)
        except IOError:
            self.ds = DataStore._empty_store
            self._set_info()

    @debugging.trace
    def _is_match(self, candidate, wanted):
        """Determine whether the 'wanted' is equal to, or a subset of
        'candidate'.

        :param candidate: the potential match string
        :param wanted: the substring that is used in search
        :returns: Return true if candidate is a match
        """

        if isinstance(candidate, bool) and isinstance(wanted, bool):
            return candidate == wanted

        candidate = candidate.lower()
        wanted = wanted.lower()

        # Exact match is easy
        if candidate == wanted:
            return True

        # Partial match occurs when the wanted string is a subset of
        # the candidate.  Note it needs to be the first part of the
        # candidate string.
        candidate_len = len(candidate)
        wanted_len = len(wanted)
        if candidate_len > wanted_len:
            if wanted[0:wanted_len] == candidate[0:wanted_len]:
                return True

        return False

    # nottested
    @debugging.trace
    def get_first_name(self, fullname):
        return self.ds[self._PEOPLE][fullname][self._META][self._FIRST]

    # nottested
    @debugging.trace
    def get_last_name(self, fullname):
        return self.ds[self._PEOPLE][fullname][self._META][self._LAST]

    # nottested
    @debugging.trace
    def get_meetings(self, fullname):
        return self.ds[self._PEOPLE][fullname][self._MEETINGS]

    @debugging.trace
    def find(self, field, value):
        """Find the persons that match the criteria.

        :param field: the field to search across all people
        :param value: the value to look for
        :returns: a list of person_idx that match
        """
        person_idxs = []
        for person_idx, d in self.ds[self._PEOPLE].iteritems():
            if self._is_match(d[self._META][field], value):
                person_idxs.append(person_idx)
        if person_idxs:
            return person_idxs
        return None

    # nottested
    def add_meeting(self, person, meeting_date):
        """Add a meeting to the supplied person.

        :param person: the person to add the meeting to
        :param meeting_date: the date of the meeting to add
        :returns: the success of the addition
        """
        # TODO(mrda): validate meeting_date
        self.ds[self._PEOPLE][person][self._MEETINGS].append(meeting_date)
        self.save()
        return True

    # nottested
    def delete_meeting(self, person, meeting_date):
        """Delete a meeting from a person.

        :param person: the person to delete the meeting from
        :param meeting_date: the date of the meeting
        :returns: the success of the addition
        """
        # TODO(mrda): validate meeting_date
        all_meeting_dates = self.ds[self._PEOPLE][person][self._MEETINGS]
        if meeting_date not in all_meeting_dates:
            print("Couldn't find {} in {}'s list of meetings".
                  format(meeting_date, person))
            return False
        cleaned = [x for x in all_meeting_dates if x != meeting_date]
        self.ds[self._PEOPLE][person][self._MEETINGS] = cleaned
        self.save()
        return True

    # notested
    def dump(self):
        print("Dumping data")
        print self.ds
