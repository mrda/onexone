#!/usr/bin/env python
#
# person - Representation of a person, part of onexone
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
from onexone import command
from onexone import datastore
from onexone import debugging

debug = False
debugging._debug = debug


class Person:
    """Representation of a person."""

    def __init__(self):
        self.c = command.CommandOptions('person')
        self.c.add_command('list', self.list, "[all]")
        self.c.add_command('add', self.add, "<first> <last> [role] [enabled]")
        self.c.add_command('enable', self.enable, "<searchstr> <enabled>")
        self.c.add_command('delete', self.delete, "(<first> <last> | <nick>)")
        self.c.add_command('find', self.find, "<search-string>")
        self.c.add_command('info', self.info, "<search-string>")

    @debugging.trace
    def _search(self, field, value):
        """Search for all persons that have 'field' set to 'value'

        :param field: the field to search for
        :param value: the value we're looking for
        :returns: The set of persons that meet the criteria, None otherwise
        """
        ds = datastore.get_datastore()
        return ds.find(field, value)

    @debugging.trace
    def _find(self, searchstr, interactive=False):
        """Search for a person based upon name, matching against the supplied
        string search criteria.

        :param searchstr: the search string to find a name match against
        :param interactive: not used
        :returns: The list of persons that match
        """
        results = set()

        result = self._search('first_name', searchstr)
        if result:
            for r in result:
                results.add(r)

        result = self._search('last_name', searchstr)
        if result:
            for r in result:
                results.add(r)

        # Search against fullname as well
        all_fullnames = datastore.get_datastore().get_all_fullnames()
        for fullname in all_fullnames:
            if searchstr in fullname:
                results.add(fullname)

        return list(results)

    @debugging.trace
    def find_person(self, person_str):
        """Search for a person based upon the supplied search string.

        :param person_str: the search criteria
        :returns: Tuple (Bool, result set | reason
        """

        # Note(mrda): Method not yet used
        possible_persons = self._find([person_str])
        len_possible_persons = len(possible_persons)
        if len_possible_persons == 0:
            return (False, "No match found")
        elif len_possible_persons != 1:
            return (False, "No unique match found")
        else:
            return (True, possible_persons[0])

    @debugging.trace
    def _exact_match(self, first, last):
        """Determine if there is an exact person match based upon the supplied
        search criteria.

        :param first: the first name to search against
        :param last: the last name to search against
        :returns: Return True if it's an exact match
        """

        first_result = self._search('first_name', first)
        if not first_result:
            return False

        last_result = self._search('last_name', last)
        if not last_result:
            return False

        intersection = [v for v in first_result if v in last_result]

        return len(intersection) == 1

    @debugging.trace
    def find(self, args):
        """Top level person find function.  Look for a person based upon the
        provided search criteria.  Print the results.

        :param args: The criteria to search against
        """
        if len(args) != 1:
            self.c.display_usage('find')
            return

        results = self._find(args[0], True)
        if results:
            print("\n".join(results))
        else:
            print("No match found")

    @debugging.trace
    def info(self, args):
        """Top level info command.  Find a person based up on the supplied
        criteria, and print all relevant information.

        :param args: the criteria to check
        """
        if len(args) != 1:
            self.c.display_usage('info')
            return

        searchstr = args[0]
        print("Searching for {}".format(searchstr))
        fullnames = self._find(searchstr, True)
        if not fullnames:
            print("No record found")
            return
        for f in fullnames:
            self._print_person(f)
        print("")

    @debugging.trace
    def _print_person(self, fullname):
        """Print all information about a person.

        :param fullname: The person to print info about
        """
        ds = datastore.get_datastore()
        print("")
        print("First name: {}".format(ds.get_first_name(fullname)))
        print("Last name: {}".format(ds.get_last_name(fullname)))
        print("Role: {}".format(ds.get_role(fullname)))
        print("Enabled?: {}".format(ds.is_enabled(fullname)))
        print("One-on-One Meetings:")
        for meeting in sorted(ds.get_meetings(fullname)):
            print("  {}".format(meeting))

    @debugging.trace
    def add(self, args):
        """Top level function for adding a person.

        :param args: list of arguments to use in building a person
        """
        len_args = len(args)
        if len_args < 2 or len_args > 4:
            self.c.display_usage('add')
            return

        role = ""

        if len_args == 2:
            first, last = args
            enabled = True
        elif len_args == 3:
            first, last, role = args
            enabled = True
        else:
            first, last, role, enabled = args

        ds = datastore.get_datastore()
        ds.new_person(first, last, role, enabled)

    @debugging.trace
    def delete(self, args):
        """Top level function for deleting a person.

        :param args: list to use in identifying the person to delete
        """
        len_args = len(args)
        if len_args < 1 or len_args > 2:
            self.c.display_usage('delete')
            return

        fullname = None
        if len_args == 1:
            # Partial user supplied, go find a match
            fullnames = self._find(args[0])
            if len(fullnames) == 0:
                print("Couldn't find person '{}' to delete".format(args[0]))
                return
            elif len(fullnames) != 1:
                print("Multiple matches, won't delete {}".format(
                      " and ".join(fullnames[0])))
                return
            fullname = fullnames[0]
        else:
            # Provided a first and last name, looking for an exact match
            first, last = args
            if self._exact_match(first, last):
                fullname = self._build_fullname((first, last))

        if raw_input("Are you sure you want to delete '{}'? ".
           format(fullname)) not in ['Y', 'y']:
            print("Not deleting user")
            return

        ds = datastore.get_datastore()
        ds.remove_entry(fullname)

    @debugging.trace
    def list(self, args):
        """Top level function for listing persons.

        :param args: list to use in identifying what to list
        """
        len_args = len(args)

        ds = datastore.get_datastore()
        if len_args == 0:
            fullnames = ds.list_fullnames()
            if fullnames is not None:
                print("\n".join(ds.list_fullnames()))
        elif len_args == 1 and args[0] == 'all':
            print(ds.list_everything())
        else:
            self.c.display_usage('list')

    @debugging.trace
    def enable(self, args):
        """Top level function to enable/disable a person.

        :param args: only two params are supported a person and enabled
        """
        len_args = len(args)
        if len_args != 2:
            self.c.display_usage('enable')
            return

        person = args[0]
        fullnames = self._find(args[0])
        if len(fullnames) == 0:
            print("Couldn't find person '{}' to enable".format(person))
            return
        elif len(fullnames) != 1:
            print("Multiple matches, won't enable {}".format(
                  " and ".join(fullnames)))
            return

        enabled = str(args[1]).lower()
        if enabled == 'true':
            enabled = True
        elif enabled == 'false':
            enabled = False
        else:
            self.c.display_usage('enable')
            return

        ds = datastore.get_datastore()
        ds.set_enabled(fullnames[0], enabled)

    @debugging.trace
    def parse(self, args):
        """Top level function to parse arguments given to the person command.
        If the person sub-command isn't recognised, print out usage.  Note that
        this command is only meant to be invoked from higher level parsing
        function.
        """
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in person.parse: {}".format(e))
