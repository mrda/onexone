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
import person

debug = False

APP_NAME = '1x1'
USER = os.environ.get('USER')
CACHE_DIR = appdirs.user_config_dir(APP_NAME, USER)
DATA_FILENAME = os.path.join(CACHE_DIR, '1x1-data.json')


def configure_datastore():
    # Initialise the location for stored data
    try:
        pathlib.Path(CACHE_DIR).mkdir(parents=True)
    except OSError as e:
        # Allow directory already exists to be squashed.
        # Otherwise allow it to bubble up
        if e.errno != os.errno.EEXIST:
            raise
    ds = datastore.choose_location(DATA_FILENAME)


def main():

    if debug:
        print("Data file location is {}".format(DATA_FILENAME))

    c = command.CommandOptions(debug=debug)
    c.add_command('person', person.person)

    configure_datastore()

    if len(sys.argv) == 1:
        c.usage()
        sys.exit(0)

    c.jump(*sys.argv[1:])


if __name__ == '__main__':
    main()
