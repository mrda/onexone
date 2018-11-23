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


class CommandOptions:

    def __init__(self, subcommand=None, debug=False):
        self.commands = {}
        self.subcommand = subcommand
        self.debug = debug
        self.quiet_commands = []

    @debugging.trace
    def add_command(self, command, func, valid_args=None, quiet=False):
        if self.debug:
            print("Registering '{}' to {}".format(command, func))
        if quiet:
            self.quiet_commands.append(command)
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

        # Special casing for bash-completion
        if command == '--list-opts':
            print(' '.join(key for key in self.commands))
            return

        try:
            func = self.commands[command][0]
            func(rest)
        except KeyError as e:
            print("Unknown subcommand: {}".format(", ".join(args)))
            self.usage()
        except Exception as e:
            print("Problem invoking subcommand '{}' ({})".format(command, e))

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
            if command in self.quiet_commands:
                continue
            print("  {} {}".format(command, self.commands[command][1]))
