from setuptools import setup, find_packages

setup(
    name='onexone',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['onexone = onexone.main:main']
        }
    )
