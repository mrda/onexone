#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = ""
#with open('README.rst') as readme_file:
#    readme = readme_file.read()
#

history = ""
#with open('HISTORY.rst') as history_file:
#    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]


setup(
    author="Michael Davies",
    author_email='michael@the-davies.net',
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
    description='Michael\'s 1x1 helper',
    entry_points={
        'console_scripts': [
	    'onexone = onexone.main:main'
	],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='onexone',
    name='onexone',
    packages=find_packages(include=['onexone']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mrda/onexone',
    version='0.2.0',
    zip_safe=False,
    )
