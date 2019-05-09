#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appdirs
from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('project_metadata.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

data_files = ['data/meeting_invite.txt', 'data/request_for_feedback.txt']

setup(
    author=main_ns['__author__'],
    author_email=main_ns['__author_email__'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description=main_ns['__description__'],
    entry_points={
        'console_scripts': [
        '{} = {}.main:main'.format(main_ns['__name__'], main_ns['__name__'])
    ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=main_ns['__name__'],
    name=main_ns['__name__'],
    packages=find_packages(include=[main_ns['__name__']]),
    data_files=[(appdirs.site_data_dir(main_ns['__name__'], 'dontcare'), data_files)],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url=main_ns['__repo__'],
    version=main_ns['__version__'],
    zip_safe=False,
    )
