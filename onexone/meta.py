#!/usr/bin/env python
#
# meta - Handle meta information
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
from onexone import utils


class Meta:
    """Handle meta information."""

    def __init__(self):
        self.c = command.CommandOptions('meta')
        self.c.add_command('list', self.list, "")
        self.c.add_command('update', self.update, "[key] [value]")

    @debugging.trace
    def list(self, args):
        utils.display_program_header()
        ds = datastore.get_datastore()
        ds.iterate_over_info(lambda k, v: print("{} = {}".format(k, v)))

    @debugging.trace
    def update(self, args):
        if len(args) != 2:
            self.c.display_usage('update')
            return
        key = args[0]
        val = args[1]

        ds = datastore.get_datastore()
        if key in ds.unupdateable_fields:
            print("*** Can't update special field '{}'".format(key))
            return

        # Data sanitisation
        bool_check = utils.sanitise_bool(val)
        if bool_check is not None:
            val = bool_check

        if ds.meta_key_exists(key):
            old_val = ds.get_meta_key(key)
            if old_val == val:
                print("--- Meta field '{}' is already set to '{}', "
                      "not changing".format(key, val))
                return
            print("--- Meta field '{}' was set to {}, now set to {}".format
                  (key, ds.get_meta_key(key), val))

        ds.update_meta(key, val)

    @debugging.trace
    def parse(self, args):
        """Top level function to parse arguments for this command.
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
            print("*** Unexpected exception in meta.parse: {}".format(e))
