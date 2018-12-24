#!/usr/bin/env python
#
# replay - Build a replay file
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


class Replay:
    """Build a replay file.

    Note: This is very dependant upon the format of the addition commands.
    If they change, this will break.

    TODO: Tie the addition commands of person/meetings/etc to the
    implementation of this class.
    """

    def __init__(self):
        self.c = command.CommandOptions('replay')
        self.c.add_command('build', self.build_replay, "")
        self.top = {'people': self.iterate_people,
                    'info': self.iterate_info,
                    }

    @debugging.trace
    def iterate_top_level(self, elem):
        self.top[elem]()

    @debugging.trace
    def iterate_people(self):
        ds = datastore.get_datastore()
        ds.iterate_over_persons(self.replay_person)

    @debugging.trace
    def replay_person(self, fullname):
        ds = datastore.get_datastore()
        start_date, end_date = ds.get_dates(fullname)
        if start_date is None:
            start_date = ""
        if end_date is None:
            end_date = ""
        print("onexone person add '{}' '{}' '{}' {} {} {}".format(
              ds.get_first_name(fullname),
              ds.get_last_name(fullname),
              ds.get_role(fullname),
              ds.get_enabled(fullname),
              start_date,
              end_date))
        meetings = ds.get_meetings(fullname)
        for m in meetings:
            print("onexone meeting add {} {}".format(fullname, m))

    @debugging.trace
    def iterate_info(self):
        ds = datastore.get_datastore()
        ds.iterate_over_info(self.replay_info)

    @debugging.trace
    def replay_info(self, key, val):
        print("onexone meta update '{}' '{}'".format(key, val))

    @debugging.trace
    def build_replay(self, filename=None):
        # TODO: Support dumping straight to file in the future
        ds = datastore.get_datastore()
        ds.iterate(self.iterate_top_level)

    @debugging.trace
    def parse(self, args):
        """Top level function to parse arguments given to the replay command.
        If the sub-command isn't recognised, print out usage.  Note that
        this command is only meant to be invoked from higher level parsing
        function.
        """
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in replay.parse: {}".format(e))
