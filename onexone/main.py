#!/usr/bin/env python
#
# onexone main.py - the main entry point for OneXOne
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
import appdirs
import errno
import pathlib
import sys

from onexone import debugging  # Must be first
from onexone import command
from onexone import datastore
from onexone import eggs
from onexone import meeting
from onexone import person
from onexone import utils


# APP_NAME = 'onexone'
# utils.register_name(APP_NAME)
# utils.register_years("2018")


@debugging.trace
def configure_datastore():
    # Initialise the location for stored data
    try:
        pathlib.Path(utils.get_config_dir()).mkdir(parents=True)
    except OSError as e:
        # Allow directory already exists to be squashed.
        # Otherwise allow it to bubble up
        if e.errno != errno.EEXIST:
            raise
    ds = datastore.choose_location(utils.get_data_filename())


def main():

    APP_NAME = 'onexone'
    utils.register_name(APP_NAME)
    utils.register_years("2018")

    c = command.CommandOptions(debug=debugging._debug)

    c.add_command('help', c.usage, "", alias=["--help"])

    c.add_command('version', utils.display_program_header, "",
                  alias=["--version"])

    c.add_command('info', utils.display_program_info, "",
                  alias=["--info"])

    p = person.Person()
    c.add_command('person', p.parse, "<subcommand>")

    e = eggs.Eggs(debug=debugging._debug)
    c.add_command(e.eggs, e.egg_info, quiet=True)

    m = meeting.Meeting()
    c.add_command('meeting', m.parse, "<subcommand>")

    configure_datastore()

    if len(sys.argv) == 1:
        c.usage()
        sys.exit(0)

    c.jump(sys.argv[1:])


if __name__ == '__main__':
    main()
