#!/usr/bin/env python
#
# main.py - main entry point for 1x1
#

import sys

import command
import datastore
import person


def main():

    c = command.CommandOptions()
    c.add_command('person', person.person)

    if len(sys.argv) == 1:
        c.usage()
        sys.exit(0)

    c.jump(*sys.argv[1:])


if __name__ == '__main__':
    main()
