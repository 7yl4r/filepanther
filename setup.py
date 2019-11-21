#!/usr/bin/env python
"""imars-etl setup.py"""

from setuptools import setup
from setuptools import find_packages
import io

# import imars_etl
# NOTE: can't do that here before dependencies installed, silly.
VERSION = '0.2.0'  # should match __version__ in imars_etl.__init__.py


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


_long_description = read('README.md')  # , 'CHANGES.txt')

_tests_require = [
    line.strip() for line in open('tests_requirements.txt')
    if line.strip() and not line.strip().startswith('--')
]

_install_requires = [
    line.strip() for line in open('requirements.txt')
    if line.strip() and not line.strip().startswith('--')
]

_extras_require = {
    'test': _tests_require
}

setup(
    name='filepanther',
    version=VERSION,
    description='Filepaths as metadata strings',
    long_description=_long_description,
    author='Tylar Murray',
    author_email='code+filepanther@tylar.info',
    url='https://github.com/7yl4r/filepanther',
    install_requires=_install_requires,
    tests_require=_tests_require,
    extras_require=_extras_require,
    entry_points={  # sets up CLI (eg bash) commands
        'console_scripts': [
            'filepanther = filepanther.__main__:_main',
        ],
    },
    # cmdclass={'test': PyTest},  # custom build commands for test/lint/etc
    packages=find_packages()  # modules added to python when installed
)
