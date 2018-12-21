#!/usr/bin/env python
#
# utils - common python package functions
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
import datetime
import os
import pkg_resources

_name = "undefined"
_years = "undefined"


def register_name(name):
    global _name
    _name = name


def register_years(years):
    global _years
    _years = years


def get_program_header():
    global _name, _years
    c = "Copyright (C) {} Michael Davies <michael-{}@the-davies.net>".format(
        _years, _name)
    return "{} Version {}  {}".format(_name,
                                      pkg_resources.require("onexone")[0]
                                      .version,
                                      c)


def get_config_dir():
    global _name
    user = os.environ.get('USER')
    config_dir = appdirs.user_config_dir(_name, user)
    return config_dir


def get_data_filename():
    global _name
    config_dir = get_config_dir()
    save_file = "{}-data.json".format(_name)
    data_filename = os.path.join(config_dir, save_file)
    return data_filename


def display_program_header(args=None):
    # Note(mrda): Ignoring args
    print(get_program_header())


def display_program_info(args=None):
    print(get_program_header())
    print("Save file location: {}".format(get_data_filename()))


def validate_date(datestr, expected="%Y%m%d"):
    try:
        dateobj = datetime.datetime.strptime(datestr, expected)
        return True
    except ValueError:
        return False


def format_string(yyyymmdd):
    if yyyymmdd == "":
        return ""
    return "{:4s}-{:2s}-{:2s}".format(yyyymmdd[0:4], yyyymmdd[4:6],
                                      yyyymmdd[6:8])
