#!/usr/bin/env python
#
# datastore - OnexOne's data representation library
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
import datetime
import json
import os

from onexone import debugging
from onexone import utils

_ds = None


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
    _ROLE = 'role'
    _MEETINGS = 'meetings'
    _START_DATE = 'start_date'
    _END_DATE = 'end_date'
    _FILENAME = 'filename'
    _VERSION = 'version'
    _LAST_MODIFIED = 'last_modified'

    required_fields = (
        _META,
        _MEETINGS,
    )

    required_meta_fields = (
        _FIRST,
        _LAST,
        _ROLE,
        _START_DATE,
        _END_DATE,
    )

    unupdateable_fields = (
        _LAST_MODIFIED,
    )

    # Note(mrda): Need to force booleans to be displayed as strings, so that
    # 'True' is printed instead of '1'.
    _all_format = "{:>15} {:>15} {!s:>15} {:>15}"

    _empty_store = {
                   _INFO: {
                       _VERSION: '',
                       _FILENAME: '',
                       _LAST_MODIFIED: '',
                          },
                   _PEOPLE: {},
                   }

    _ds_version = {
        'major': 1,
        'minor': 3,
        'patch': 0,
    }

    def __init__(self, filename):
        self.ds = {}
        self.filename = filename
        self.load(self.filename)

    # notested
    @debugging.trace
    def build_fullname(self, first, last):
        """Build a fullname from the supplied first and last name.

        :param first: the person's first name
        :param last: the person's last name
        :returns: the combined fullname
        """
        fullname = None if first is None else first
        if last is not None:
            fullname += last
        return fullname

    # notested
    def meta_key_exists(self, key):
        return key in self.ds[self._INFO]

    # notested
    def update_meta(self, key, val):
        self.ds[self._INFO][key] = val
        self.save(self.filename)

    # notested
    def get_meta_key(self, key):
        return self.ds[self._INFO].get(key, None)

    # notested
    def person_exists(self, fullname):
        return fullname in self.ds[self._PEOPLE]

    # notested
    def update_person(self, fullname, key, val):
        # TODO: Should be returning back errors and not printing them here
        if fullname not in self.ds[self._PEOPLE]:
            print("*** Can't find '{}' to update".format(fullname))
            return
        if key not in self.ds[self._PEOPLE][fullname][self._META]:
            print("*** Can't find '{}' in person '{}' to update".format
                  (key, fullname))
            print("*** Valid fields are: {}".format(", ".join(
                  sorted(self.ds[self._PEOPLE][fullname][self._META].keys()))))
            return

        # TODO: Validate 'val' for date type etc
        bool_check = utils.sanitise_bool(val)
        if bool_check is not None:
            val = bool_check

        self.ds[self._PEOPLE][fullname][self._META][key] = val
        self.save(self.filename)

    # notested
    def new_person(self, first, last, role, start_date, end_date):
        """Add a new person.

        :param first: the person's first name
        :param last: the person's last name
        :param role: the person's role
        :param start_date: the person's start_date
        :param end_date: the person's end_date
        """
        person = {}
        person[self._META] = {}
        person[self._META][self._FIRST] = first
        person[self._META][self._LAST] = last
        person[self._META][self._ROLE] = role
        person[self._META][self._START_DATE] = start_date
        # Clearly adding a person won't have an end date, but we want
        # to make sure this field is created
        person[self._META][self._END_DATE] = end_date
        person[self._MEETINGS] = ()

        fullname = self.build_fullname(first, last)
        self.ds[self._PEOPLE][fullname] = person
        self.save(self.filename)

    # notested
    def remove_entry(self, key):
        # Note(mrda): No error if key isn't in dict
        self.ds[self._PEOPLE].pop(key, None)
        self.save(self.filename)

    # notested
    def ensure_fields(self):
        # Iterate over all data, ensuring all fields are present
        for key in sorted(self.ds[self._PEOPLE].keys()):
            for req_field in self.required_fields:
                try:
                    a = self.ds[self._PEOPLE][key][req_field]
                except KeyError:
                    self.ds[self._PEOPLE][key][req_field] = None
            for req_meta_field in self.required_meta_fields:
                try:
                    a = self.ds[self._PEOPLE][key][self._META][req_meta_field]
                except KeyError:
                    self.ds[self._PEOPLE][key][self._META][req_meta_field] \
                        = None
        # Update the version string
        self.ds[self._INFO][self._VERSION] = self._make_version()

    def _make_version(self):
        return "{}.{}.{}".format(DataStore._ds_version['major'],
                                 DataStore._ds_version['minor'],
                                 DataStore._ds_version['patch'])

    def _set_info(self):
        self.ds[self._INFO][self._VERSION] = self._make_version()
        self.ds[self._INFO][self._FILENAME] = self.filename

    def version(self):
        return self.ds[self._INFO][self._VERSION]

    def list_fullnames(self, enabled=True):
        all_fullnames = set()
        for fullname in sorted(self.ds[self._PEOPLE].keys()):
            ed = self.ds[self._PEOPLE][fullname][self._META][self._END_DATE]
            if enabled:
                if self.is_enabled(fullname):
                    all_fullnames.add(fullname)
            else:
                # We want disabled persons
                if not self.is_enabled(fullname):
                    all_fullnames.add(fullname)

        if len(all_fullnames) == 0:
            return None

        return all_fullnames

    @debugging.trace
    def iterate(self, func):
        """Iterate over the top-level structure.

        :param func: The function to invoke
        """
        for elem in self.ds:
            func(elem)

    @debugging.trace
    def iterate_over_info(self, func):
        """Iterate over all info fields, invoking func.

        :param func: The function to invoke, which takes a key/value pair
        """
        for key, val in sorted(self.ds[self._INFO].items()):
            func(key, val)

    @debugging.trace
    def iterate_over_persons(self, func, enable_state=None):
        """Iterate over all persons, invoking func.

        :param func: The function to invoke, which takes a fullname as a param
        :param enable_state: one of None, 'enable', 'disable'
        """

        # If we supply an enable_state, that will be honoured
        # If we don't supply an enable_state, invoke the function anyways

        if enable_state is None or enable_state == 'enable':
            enable = True
        elif enable_state == 'disable':
            enable = False

        for fullname in sorted(self.ds[self._PEOPLE].keys()):
            if enable_state is None:
                func(fullname)
            else:
                ed = (self.ds[self._PEOPLE][fullname][self._META]
                             [self._END_DATE])
                if enable_state == 'enable':
                    # Only want persons who don't have an end date
                    if self.is_enabled(fullname):
                        func(fullname)
                else:
                    # Only want persons who do have an end date
                    if not self.is_enabled(fullname):
                        func(fullname)

    def is_enabled(self, fullname):
        """Check to see if a person is enabled.

        :param fullname: the name to check
        :returns: Return true if the person is enabled
        """
        ed = self.ds[self._PEOPLE][fullname][self._META][self._END_DATE]
        return ed is None or ed == ""

    def get_all_fullnames(self):
        """Return all fullnames as a list."""
        return list(self.ds[self._PEOPLE].keys())

    def get_meetings(self, key):
        return self.ds[key][self._MEETINGS]

    def save(self, filename):
        self.ds[self._INFO][self._LAST_MODIFIED] = \
            datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        with open(filename, "w") as f:
            json.dump(self.ds, f, indent=4)

    def build_savefile(self, filename):
        fmt = '%Y%m%d'
        today = datetime.date.today()
        return "{}-{}".format(filename, today.strftime(fmt))

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                self.ds = json.load(f)

            # We need to cater for changing schema definitions.  The easiest
            # and most backwards-compatible way is to ensure we have all the
            # required fields available for each record.
            self.ensure_fields()

            # Now that the file successfully opened, let's save a copy before
            # we do anything as a backup if we don't have one for today already
            backup_filename = self.build_savefile(filename)
            if not os.path.isfile(backup_filename):
                self.save(backup_filename)

        except IOError:
            # There is no savefile, so start one
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

    @debugging.trace
    def get_first_name(self, fullname):
        try:
            return self.ds[self._PEOPLE][fullname][self._META][self._FIRST]
        except KeyError:
            return None

    @debugging.trace
    def get_last_name(self, fullname):
        try:
            return self.ds[self._PEOPLE][fullname][self._META][self._LAST]
        except KeyError:
            return None

    # nottested
    @debugging.trace
    def get_role(self, fullname):
        try:
            return self.ds[self._PEOPLE][fullname][self._META][self._ROLE]
        except KeyError:
            return None

    # nottested
    @debugging.trace
    def get_enabled(self, fullname):
        try:
            return (not self.ds[self._PEOPLE][fullname][self._META]
                               [self._END_DATE])
        except KeyError:
            return False

    # nottested
    @debugging.trace
    def get_dates(self, fullname):
        try:
            return (
                self.ds[self._PEOPLE][fullname][self._META][self._START_DATE],
                self.ds[self._PEOPLE][fullname][self._META][self._END_DATE])
        except KeyError:
            return None

    @debugging.trace
    def get_meetings(self, fullname):
        try:
            return self.ds[self._PEOPLE][fullname][self._MEETINGS]
        except KeyError:
            return None

    @debugging.trace
    def find(self, field, value):
        """Find the persons that match the criteria.

        :param field: the field to search across all people
        :param value: the value to look for
        :returns: a list of person_idx that match
        """
        person_idxs = []
        for person_idx, d in self.ds[self._PEOPLE].items():
            if self._is_match(d[self._META][field], value):
                person_idxs.append(person_idx)
        if person_idxs:
            return person_idxs
        return None

    # notested
    def meeting_exists(self, fullname, meeting):
        return meeting in self.ds[self._PEOPLE][fullname][self._MEETINGS]

    # nottested
    def add_meeting(self, person, meeting_date):
        """Add a meeting to the supplied person.

        :param person: the person to add the meeting to
        :param meeting_date: the date of the meeting to add
        :returns: the success of the addition
        """
        # TODO(mrda): validate meeting_date
        self.ds[self._PEOPLE][person][self._MEETINGS].append(meeting_date)
        self.save(self.filename)
        return True

    # nottested
    def delete_meeting(self, person, meeting_date):
        """Delete a meeting from a person.

        :param person: the person to delete the meeting from
        :param meeting_date: the date of the meeting
        :returns: the success of the addition
        """
        # TODO: validate meeting_date
        # TODO: Should be returning back errors and not printing them here
        all_meeting_dates = self.ds[self._PEOPLE][person][self._MEETINGS]
        if meeting_date not in all_meeting_dates:
            print("Couldn't find {} in {}'s list of meetings".
                  format(meeting_date, person))
            return False
        cleaned = [x for x in all_meeting_dates if x != meeting_date]
        self.ds[self._PEOPLE][person][self._MEETINGS] = cleaned
        self.save(self.filename)
        return True

    def dump(self):
        print("Dumping data")
        print(self.ds)
