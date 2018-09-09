
import pkg_resources

_name = "undefined"
_years = "undefined"


def register_name(name):
    global _name
    _name = name


def register_years(years):
    global _years
    _years = years


def display_program_header(args=None):
    # Note(mrda): Ignoring args
    global _name, _years
    c = "Copyright (C) {} Michael Davies <michael-{}@the-davies.net>".format(
        _years, _name)
    print("{} Version {}  {}".format(_name,
                                     pkg_resources.require("1x1")[0].version,
                                     c))
