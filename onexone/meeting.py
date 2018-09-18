#!/usr/bin/env python
#
# meeting - Representation of a meeting, part of onexone
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
import person

debug = False
debugging._debug = debug


class Meeting:
    """Representation of a meeting."""

    def __init__(self):
        self.c = command.CommandOptions('meeting')
        self.c.add_command('add', self.add, "<person> <date>")
        self.c.add_command('delete', self.delete, "<person> <date>")
        self.c.add_command('up-next', self.up_next, "")
        self.p = person.Person()

    @debugging.trace
    def add(self, args):
        """Add a meeting to a person.

        :param person: a match string of a person
        :param meeting: the meeting date to add
        """
        len_args = len(args)
        if len_args != 2:
            self.c.display_usage('add')
            return

        name = args[0]
        meeting = args[1]
        matches = self.p._find([name], False)
        if not matches:
            print("Can't find '{}'".format(name))
            return
        if len(matches) > 1:
            print("Multiple persons found: {}".format(matches))
            return
        # Note(mrda): Shouldn't be playing with the internals of
        # entries here.  We need code to abstract this
        ds = datastore.get_datastore()
        dictionary = ds.get_dict()
        dictionary[matches[0]]['meetings'].append(meeting)
        ds.save()

    @debugging.trace
    def delete(self, args):
        """Delete a meeting from a person.

        :param person: a match string of a person
        :param meeting: the meeting date to delete
        """
        len_args = len(args)
        if len_args != 2:
            self.c.display_usage('delete')
            return

        name = args[0]
        meeting = args[1]
        matches = self.p._find([name], False)
        if not matches:
            print("Can't find '{}'".format(name))
            return
        if len(matches) > 1:
            print("Multiple persons found: {}".format(matches))
            return
        # Note(mrda): Shouldn't be playing with the internals of
        # entries here.  We need code to abstract this
        ds = datastore.get_datastore()
        dictionary = ds.get_dict()
        all_meetings = dictionary[matches[0]]['meetings']
        if meeting not in all_meetings:
            print("Couldn't find {} in {}'s list of meetings".
                  format(meeting, person))
            return
        cleaned = [x for x in all_meetings if x != meeting]
        dictionary[matches[0]]['meetings'] = cleaned
        ds.save()

    @debugging.trace
    def get_latest_meeting(self, nick):
        """Find the last meeting a person had.

        :param: nick the person to search
        """
        ds = datastore.get_datastore()

        mtgs = ds.get_meetings(nick)
        if not mtgs:
            return None

        meetings = sorted(mtgs, reverse=True)
        return meetings[0]

    @debugging.trace
    def up_next(self, args):
        """ Find the next person who are up next for a meeting.

        :param args: ignored
        """
        # Note(mrda): Ignoring args

        # Get the latest meeting slot for each person who is enabled
        ds = datastore.get_datastore()
        last_meeting = {}
        for nick in ds.ds.keys():
            if not self.p.is_enabled(nick):
                continue
            mtg = self.get_latest_meeting(nick)
            if not mtg:
                mtg = 0

            last_meeting[nick] = mtg

        # Sort list in reverse chronological order
        people_meetings = sorted(last_meeting.iteritems(),
                                 key=lambda (k, v): (v, k))

        # Display
        format_str = "{:>{}}  {:>8}"
        max_name_len = 0

        # Find longest name first
        for pm in people_meetings:
            if len(pm[0]) > max_name_len:
                max_name_len = len(pm[0])

        print(format_str.format("Name", max_name_len, "Last OneOnOne"))
        print(format_str.format("----", max_name_len, "-------------"))
        for pm in people_meetings:
            # TODO(mrda): Resolve why this needs to be compared to True
            if self.p.is_enabled(pm[0]) is True:
                meeting = "never"
                if pm[1] != 0:
                    meeting = pm[1]
                print(format_str.format(pm[0], max_name_len, meeting))

    @debugging.trace
    def parse(self, args):
        """Top level function to parse arguments given to the meeting command.
        If the meeting sub-command isn't recognised, print out usage.  Note
        that this command is only meant to be invoked from higher level parsing
        function.
        """
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in meeting.parse: {}".format(e))
