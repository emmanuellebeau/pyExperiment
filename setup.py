#! /usr/bin/env python
#
# Copyright (C) 2018 Daniel Lindh <p.j.d.lindh@uva.nl>


import os
import subprocess

# we are using a setuptools namespace
import setuptools  # analysis:ignore
from setuptools import find_packages
from numpy.distutils.core import setup

descr = """python Experiment package."""

DISTNAME = 'pyExperiment'
DESCRIPTION = descr
MAINTAINER = 'Daniel Lindh'
MAINTAINER_EMAIL = 'p.j.d.lindh@uva.nl'
URL = 'https://github.com/lajnd/pyExperiment'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/lajnd/pyExperiment'

# version
version_file = os.path.join('pyExperiment', '_version.py')
with open(version_file, 'r') as fid:
    line = fid.readline()
    VERSION = line.strip().split(' = ')[1][1:-1]


def git_version():
    """Helper adapted from Numpy"""
    def _minimal_ext_cmd(cmd):
        # minimal env; LANGUAGE is used on win32
        return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                ).communicate()[0]
    GIT_REVISION = 'Unknown'
    if os.path.exists('.git'):
        try:
            out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
            GIT_REVISION = out.decode('utf-8').strip()
        except OSError:
            pass
    return GIT_REVISION[:7]


FULL_VERSION = VERSION + '+' + git_version()


def write_version(version):
    with open(version_file, 'w') as fid:
        fid.write('__version__ = \'{0}\'\n'.format(version))


def setup_package(script_args=None):
    """Actually invoke the setup call"""
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')
    with open('README.md') as fid:
        long_description = fid.read()
    kwargs = dict(
        name=DISTNAME,
        maintainer=MAINTAINER,
        include_package_data=True,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=FULL_VERSION,
        download_url=DOWNLOAD_URL,
        long_description=long_description,
        zip_safe=False,  # the package can run out of an .egg file
        classifiers=['Intended Audience :: Science/Research',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved',
                     'Programming Language :: Python',
                     'Topic :: Software Development',
                     'Topic :: Scientific/Engineering',
                     'Operating System :: Unix',
                     'Operating System :: MacOS'],
        platforms='any',
        packages= find_packages(),
        scripts=[])
    if script_args is not None:
        kwargs['script_args'] = script_args
    try:
        write_version(FULL_VERSION)
        setup(**kwargs)
    finally:
        write_version(VERSION)


if __name__ == '__main__':
    setup_package()
