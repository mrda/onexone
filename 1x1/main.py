#!/usr/bin/env python
#
# main.py - main entry point for 1x1
#

import appdirs
import os
import pathlib
import sys

import command
import datastore
import debugging
import meeting
import person

debug = False

APP_NAME = '1x1'
USER = os.environ.get('USER')
CONFIG_DIR = appdirs.user_config_dir(APP_NAME, USER)
DATA_FILENAME = os.path.join(CONFIG_DIR, '1x1-data.json')


@debugging.trace
def configure_datastore():
    # Initialise the location for stored data
    try:
        pathlib.Path(CONFIG_DIR).mkdir(parents=True)
    except OSError as e:
        # Allow directory already exists to be squashed.
        # Otherwise allow it to bubble up
        if e.errno != os.errno.EEXIST:
            raise
    ds = datastore.choose_location(DATA_FILENAME)


def main():

    c = command.CommandOptions(debug=debug)
    p = person.Person()
    c.add_command('person', p.parse, "<subcommand>")
    c.add_command('meeting', meeting.meeting, "<subcommand>")

    configure_datastore()

    if len(sys.argv) == 1:
        c.usage()
        sys.exit(0)

    c.jump(sys.argv[1:])


if __name__ == '__main__':
    main()
