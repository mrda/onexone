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
import command
import datastore
import debugging

debug = False
debugging._debug = debug


class Person:
    """Representation of a person."""

    def __init__(self):
        self.c = command.CommandOptions('person')
        self.c.add_command('list', self.list, "[all]")
        self.c.add_command('add', self.add, "<first> <last> [enabled]")
        self.c.add_command('delete', self.delete, "(<first> <last> | <nick>)")
        self.c.add_command('find', self.find, "<search-string>")
        self.c.add_command('info', self.info, "<search-string>")

    @debugging.trace
    def _is_match(self, candidate, wanted):
        """Determine whether the 'wanted' is equal to, or a subset of
        'candidate'.

        :param candidate: the potential match string
        :param wanted: the substring that is used in search
        :returns: Return true if candidate is a match
        """
        # Note(mrda): Need to imlement case insensitive comparison

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
    def _search(self, field, value):
        """Search for all persons that have 'field' set to 'value'

        :param field: the field to search for
        :param value: the value we're looking for
        :returns: The set of persons that meet the criteria, None otherwise
        """

        results = []
        try:
            ds = datastore.get_datastore()
            dictionary = ds.get_dict()
            for k, v in dictionary.iteritems():
                # TODO(mrda): Need to handle key not in dict
                if self._is_match(v['meta'][field], value):
                    results.append(k)
            if results:
                return results
            return None
        except Exception as e:
            print("An exception got raised, {}".format(e))
            return None

    @debugging.trace
    def _find(self, args, interactive=False):
        """Search for a person based upon name, matching against the supplied
        string search criteria.

        :param args: the search string to look for
        :param interactive: not used
        :returns: The list of persons that match
        """
        results = []

        result = self._search('first_name', args[0])
        if result:
            for r in result:
                results.append(r)

        result = self._search('last_name', args[0])
        if result:
            for r in result:
                results.append(r)

        # TODO(mrda): Should search against nick as well

        return results

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

        results = self._find(args, True)
        if results:
            print("\n".join(results))
        else:
            print("No match found")

    @debugging.trace
    def is_enabled(self, nick):
        """Check to see if a person is enabled.

        :param nick: the nick to check
        :returns: Return true if the person is enabled
        """
        ds = datastore.get_datastore()
        dictionary = ds.get_value(nick)
        return dictionary['meta']['enabled']

    @debugging.trace
    def info(self, args):
        """Top level info command.  Find a person based up on the supplied
        criteria, and print all relevant information.

        :param args: the criteria to check
        """
        if len(args) != 1:
            self.c.display_usage('info')
            return

        nick = self._find(args, False)
        if not nick:
            print("No record found")
            return
        for n in nick:
            self._print_person(n)
        print("")

    @debugging.trace
    def _print_person(self, nick):
        """Print all information about a person.

        :param nick: The person to print info about
        """
        ds = datastore.get_datastore()
        dictionary = ds.get_value(nick)
        print("")
        print("First name: {}".format(dictionary['meta']['first_name']))
        print("Last name: {}".format(dictionary['meta']['last_name']))
        print("Enabled?: {}".format(dictionary['meta']['enabled']))
        print("One-on-One Meetings:")
        for entry in sorted(dictionary['meetings']):
            print("  {}".format(entry))

    @debugging.trace
    def _build_nick(self, args):
        """Build a nick from the supplied (first, last) list.

        :param args: a list of (first, last)
        """
        nick = None if args[0] is None else args[0]
        if len(args) > 1:
            nick += args[1]
        return nick

    @debugging.trace
    def _new_person(self, first=None, last=None, enabled=True):
        """Build up the data representation of a person.

        :param first: the person's first name
        :param last: the person's last name
        :param enabled: whether the individual is enabled

        :returns: the dict representing a person
        """
        p = {}
        p['meta'] = {}
        p['meta']['enabled'] = enabled
        p['meta']['first_name'] = first
        p['meta']['last_name'] = last
        p['meetings'] = ()

        return p

    @debugging.trace
    def add(self, args):
        """Top level function for adding a person.

        :param args: list of arguments to use in building a person
        """
        len_args = len(args)
        if len_args < 2 or len_args > 3:
            self.c.display_usage('add')
            return

        if len_args == 2:
            first, last = args
            enabled = True
        else:
            first, last, enabled = args

        ds = datastore.get_datastore()
        ds.new_entry(self._build_nick(args),
                     self._new_person(first, last, enabled))
        ds.save()

    @debugging.trace
    def delete(self, args):
        """Top level function for deleting a person.

        :param args: list to use in identifying the person to delete
        """
        len_args = len(args)
        if len_args < 1 or len_args > 2:
            self.c.display_usage('delete')
            return

        nick = None
        if len_args == 1:
            # Partial user supplied, go find a match
            nick = self._find(args)
            if len(nick) == 0:
                print("Couldn't find person '{}' to delete".format(args[0]))
                return
            elif len(nick) != 1:
                print("Multiple matches, won't delete {}".format(
                      " and ".join(nick)))
                return
        else:
            # Provided a first and last name, looking for an exact match
            first, last = args
            if self._exact_match(first, last):
                nick = self._build_nick((first, last))

        if raw_input("Are you sure you want to delete '{}'? ".
           format(nick[0])) not in ['Y', 'y']:
            print("Not deleting user")
            return

        ds = datastore.get_datastore()
        ds.remove_entry(nick[0])
        ds.save()

    @debugging.trace
    def list(self, args):
        """Top level function for listing persons.

        :param args: list to use in identifying what to list
        """
        len_args = len(args)

        ds = datastore.get_datastore()
        if len_args == 0:
            ds.list_keys()
        elif len_args == 1 and args[0] == 'all':
            ds.list_everything()
        else:
            self.c.display_usage('list')

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
