#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Zhe Zhang, zzxuanyuan@gmail.com
#
# This setup script is part of the project that optimize redundancy between application and storage is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

import re

from setuptools import setup, find_packages


def get_version():
	"""Parse __init__.py for version number instead of importing the file."""
	VERSIONFILE = 'minredundancy/__init__.py'
	VSRE = r'^__version__ = [\'"]([^\'"]*)[\'"]'
	with open(VERSIONFILE) as f:
		verstrline = f.read()
	mo = re.search(VSRE, verstrline, re.M)
	if mo:
		return mo.group(1)
	raise RuntimeError('Unable to find version in {fn}'.format(fn=VERSIONFILE))


LONG_DESCRIPTION = """
``minredundancy`` is a module to optimize redundancy between application and storage.

Visit the `project page <https://github.com/zzxuanyuan/minredundancy>`_ for
additional information and documentation.

**Example Usage**
"""

setup(
	name='minredundancy',
	version=get_version(),
	author='Zhe Zhang',
	author_email='zzxuanyuan@gmail.com',
	url='https://github.com/zzxuanyuan/minredundancy',
	description='Optimizing redundancy between application and storage',
	long_description=LONG_DESCRIPTION,
	license='BSD',
	classifiers=[
		'Development Status :: 0.1',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Topic :: Redundancy',
		'Topic :: Software Development',
		],
	packages=find_packages(exclude=('tests',)),
	entry_points={}
)
