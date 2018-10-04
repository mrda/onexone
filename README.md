# One on One

A simple command-line tool to help people managers herd the cats.

## Quick Start

To build a start environment, just do the following:

    make
    
If this is your first time, it will prompt you to do the following:

    . ./venv/bin/activate

Once you've started the virtual environment, just start over:

    make develop

## CLI Usage

* `onexone help` - Provides online help
* `onexone version` - Displays the software version

* `onexone person add <first> <last> [enabled]` - Add a person to be managed, optionally specifying whether they are enabled or disabled.  By default, new people added are enabled.
* `onexone person delete (<first> <last>|<nick>)` - Search and delete a person
* `onexone person find <search-str>` - Search and find a person
* `onexone person info <search-str>` - Display all info about a person
* `onexone person list [all]` - Display all people managed by onexone, optionally displaying everything about them.

* `onexone meeting add <person> <date>` - Add a One-on-One meeting to person
* `onexone meeting up-next` - Display the order of people to have a One-on-One meeting with

## Help

You can try contacting Michael Davies <michael-onexone@the-davies.net>

