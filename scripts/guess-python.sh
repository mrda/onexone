#!/bin/sh
#
# guess-python.sh - Work out whether we have python 2 or
#                   python 3 available to us.  If we have both,
#                   prefer python3, because it is the future :-)
#
# Copyright (C) 2018 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
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
check_cmd ()
{
    hash ${1} &> /dev/null
    return $?
}

check_cmd python
CHECK_PY=$?
if [ ${CHECK_PY} -ne 0 ]; then
    echo "none"
    exit 1
fi

check_cmd python3
CHECK_PY=$?
if [ ${CHECK_PY} -eq 0 ]; then
    echo "python3"
    exit 0
fi

PY_MAJOR=$(python -c "import sys; print(sys.version_info.major)")

if [ ${PY_MAJOR} -eq 3 ]; then
    echo "python3"
    exit 0
fi

if [ ${PY_MAJOR} -eq 2 ]; then
    echo "python2"
    exit 0
fi
