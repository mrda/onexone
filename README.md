# One on One
[![License: GPL v3+](https://img.shields.io/badge/license-GPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/mrda/onexone.svg?branch=master)](https://travis-ci.com/mrda/onexone)

A simple command-line tool to help people managers herd the cats.

## Quick Start

To build a developer environment, just do the following:

    make
    
If this is the first time you've run this in this terminal, it will prompt you to start the virtual environment that was created for you.  You can do this as follows:

    . ./venv/bin/activate

Once you've started the virtual environment, just start over:

    make 
    
The build system will automatically determine if python3 is available, and if so, it will set things up for you to use that - but if it isn't, it will fall back and use python2 instead.

## CLI Usage

* `onexone help` - Provides online help
* `onexone version` - Displays the software version

* `onexone person add <first> <last> [role] [enabled] [start-date] [end-date]` - Add a person to be managed, optionally specifying their role, whether they are enabled or disabled, and their start and end dates.  By default, new people added are enabled.
* `onexone person delete (<first> <last>|<nick>)` - Search and delete a person
* `onexone person enable <searchstrst> <enabled>` - Enable or disable a person
* `onexone person find <search-str>` - Search and find a person
* `onexone person info <search-str>` - Display all info about a person
* `onexone person list [all]` - Display all people managed by onexone, optionally displaying everything about them.

* `onexone meeting add <person> <date>` - Add a One-on-One meeting to a person
* `onexone meeting delete <person> <date>` - Delete a One-on-One meeting from a person
* `onexone meeting up-next` - Display the order of people to have a One-on-One meeting with

## Help

You can try contacting Michael Davies <michael-onexone@the-davies.net>

