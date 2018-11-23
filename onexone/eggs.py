#!/usr/bin/env python
#
# eggs - Handle eggs
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

from onexone import debugging

from codecs import encode as z
from builtins import chr


class Eggs:

    def __init__(self, debug):
        self.debug = debug
        self.y = chr(175) + chr(92) + chr(95) + chr(40) + chr(12484)
        self.y += chr(41) + chr(95) + chr(47) + chr(175)
        self.z = chr(114) + chr(111) + chr(116) + chr(95) + chr(49) + chr(51)
        self.eggs = chr(104) + chr(111) + chr(119)

    @debugging.trace
    def egg_info(self, args):
        if (len(args) == 4 and
           z(args[0], self.z) == 'qb' and
           z(args[1], self.z) == 'V' and
           z(args[2], self.z) == 'znantr' and
           z(args[3], self.z) == 'crbcyr?'):
            print(self.y)
        else:
            args.insert(0, self.eggs)
            print("Unknown subcommand: {}".format(", ".join(args)))
            self.usage()

    def usage(self):
        print("Nothing to see here, move along...")
