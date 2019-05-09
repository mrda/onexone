#!/usr/bin/env python
#
# template - Provide a way to get templates for 1x1s easily
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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

import appdirs
from onexone import command
from onexone import debugging
from onexone import utils


class Template:

    def __init__(self):
        self.c = command.CommandOptions('template')
        self.c.add_command('request_for_feedback', self.request_for_feedback,
                           '')
        self.c.add_command('meeting_invite', self.meeting_invite, '')

    @debugging.trace
    def request_for_feedback(self, args):
        """Display a request_for_feedback template """
        len_args = len(args)
        if len_args != 0:
            self.c.display_usage('request_for_feedback')
            return
        self.print_template("request_for_feedback.txt")

    @debugging.trace
    def meeting_invite(self, args):
        """Display a meeting invite """
        len_args = len(args)
        if len_args != 0:
            self.c.display_usage('meeting_invite')
            return
        self.print_template("meeting_invite.txt")

    @debugging.trace
    def print_template(self, filename):

        # We'll first look in the user's data directory
        # and fall back to the site location if we can't find what
        # we're looking for
        site_data_dir = utils.get_site_data_dir()
        user_data_dir = utils.get_user_data_dir()
        # TODO(mrda): Check for files and fall through
        print("print_template: asked to display {}".format(filename))
        print("print_template: site_data_dir {}".format(site_data_dir))
        print("print_template: user_data_dir {}".format(user_data_dir))

    @debugging.trace
    def parse(self, args):
        """Top level function to parse arguments given to the template command.
        If the template sub-command isn't recognised, print out usage.  Note
        that this command is only meant to be invoked from higher level parsing
        function.
        """
        try:
            if len(args) == 0:
                self.c.usage()
                return
            self.c.jump(args)
        except Exception as e:
            print("*** Unexpected exception in template.parse: {}".format(e))
