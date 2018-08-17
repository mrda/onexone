from setuptools import setup, find_packages

setup(
    name='1x1',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['1x1 = 1x1.main:main']
        }
    )
