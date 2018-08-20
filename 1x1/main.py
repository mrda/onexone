#!/usr/bin/env python
#
# main.py - main entry point for 1x1
#

import sys

import command
import datastore


debug = False

_ds = None


def get_datastore(filename="1x1-data"):
    global _ds
    if _ds is None:
        _ds = datastore.DataStore(filename)
    return _ds


def person(command, arg=None):
    if debug:
        print("Entering person: command = {}, name = {}".
              format(command, arg))
    try:
        if command == 'add':
            ds = get_datastore()
            ds.new_entry(arg)
            ds.save()
        elif command == 'list':
            ds = get_datastore()
            ds.list_entries()

    except Exception as e:
        print("Error in person: {}".format(e))


def main():

    print("Welcome to 1x1")

    c = command.CommandOptions()
    c.add_command('person', person)
    c.jump(*sys.argv[1:])


if __name__ == '__main__':
    main()
