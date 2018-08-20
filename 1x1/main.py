#!/usr/bin/env python
#
# main.py - main entry point for 1x1
#

import sys

import command
import datastore
import person

debug = False


def main():

    print("Welcome to 1x1")

    c = command.CommandOptions()
    c.add_command('person', person.person)
    c.jump(*sys.argv[1:])


if __name__ == '__main__':
    main()
