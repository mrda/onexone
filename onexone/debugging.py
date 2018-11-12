#!/usr/bin/env python
#
# debugging - Simple debugging aids
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
import functools
import sys

_debug = False


for arg in sys.argv:
    if arg == "--debug":
        _debug = True


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('TRACE: Calling {}() with {}, {}'
              .format(func.__name__, args, kwargs))
        original_result = func(*args, **kwargs)
        print('TRACE: {}() returned {}'.format(func.__name__, original_result))
        return original_result
    if _debug:
        return wrapper
    else:
        return func
