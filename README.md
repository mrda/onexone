# One on One

A simple command-line tool to help people managers herd the cats.

## Quick Start

    make venv
    . ./venv/bin/activate
    make develop
    make check
    make tests

## CLI Usage

* `oneonone help` - Provides online help
* `oneonone version` - Displays the software version

* `oneonone person add <first> <last> [enabled]` - Add a person to be managed, optionally specifying whether they are enabled or disabled.  By default, new people added are enabled.
* `oneonone person delete (<first> <last>|<nick>)` - Search and delete a person
* `oneonone person find <search-str>` - Search and find a person
* `oneonone person info <search-str>` - Display all info about a person
* `oneonone person list [all]` - Display all people managed by oneonone, optionally displaying everything about them.

* `oneonone meeting add <person> <date>` - Add a One-on-One meeting to person
* `oneonone meeting up-next` - Display the order of people to have a One-on-One meeting with

## Help

You can try contacting Michael Davies <michael-oneonone@the-davies.net>

