#!/usr/bin/env python
#
# command.py - really basic command line processing library
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
from onexone import debugging
from onexone import utils

from codecs import encode as z
from builtins import chr


class CommandOptions:

    def __init__(self, subcommand=None, debug=False):
        self.commands = {}
        self.subcommand = subcommand
        self.debug = debug
        self.y = chr(175) + chr(92) + chr(95) + chr(40) + chr(12484)
        self.y += chr(41) + chr(95) + chr(47) + chr(175)
        self.z = chr(114) + chr(111) + chr(116) + chr(95) + chr(49) + chr(51)
        self.eggs = chr(104) + chr(111) + chr(119)
        self.commands[self.eggs] = (self.egg_info, None)

    @debugging.trace
    def add_command(self, command, func, valid_args=None):
        if self.debug:
            print("Registering '{}' to {}".format(command, func))
        self.commands[command] = (func, valid_args)
        if self.debug:
            self.show_jumptable()
            print("\n")

    def get_commands(self):
        return sorted(self.commands.keys())

    @debugging.trace
    def jump(self, args):
        command = args[0]
        rest = args[1:]
        if self.debug:
            print("jump: About to invoke '{}' with args '{}'".
                  format(command, rest))
        try:
            func = self.commands[command][0]
            func(rest)
        except KeyError as e:
            print("Unknown subcommand: {}".format(", ".join(args)))
            self.usage()
        except Exception as e:
            print("Problem invoking subcommand '{}' ({})".format(command, e))

    @debugging.trace
    def egg_info(self, args):
        if (len(args) == 4 and
           z(args[0], self.z) == 'qb' and
           z(args[1], self.z) == 'V' and
           z(args[2], self.z) == 'znantr' and
           z(args[3], self.z) == 'crbcyr?'):
            print(self.y)
        else:
            args.insert(0, self.eggs)
            print("Unknown subcommand: {}".format(", ".join(args)))
            self.usage()

    def show_jumptable(self):
        print("==== Jump table ====")
        print(self.commands)

    def display_usage(self, command):
        if command not in self.commands:
            print("*** No such subcommand defined")
            return
        print("Usage: {} {}".format(command, self.commands[command][1]))

    def usage(self, args=None):
        # Note(mrda): Deliberately ignoring args
        utils.display_program_header()
        if self.subcommand:
            print("Valid subcommands for '{}' are:".format(self.subcommand))
        else:
            print("Valid commands are:")
        for command in sorted(self.commands.keys()):
            if command == self.eggs:
                continue
            print("  {} {}".format(command, self.commands[command][1]))
