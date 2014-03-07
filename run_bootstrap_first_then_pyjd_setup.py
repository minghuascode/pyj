# Copyright (C) 2009, 2014 Luke Kenneth Casson Leighton <lkcl@lkcl.net>
# See LICENSE for details.

from distutils.core import setup

import os
import sys

version = os.environ.get('VERSION', open('VERSION', 'rt').read().strip())

keyw = """\
pyjamas
"""
if __name__ == '__main__':

    print >> sys.stderr, """
    Have you run bootstrap.py to create bin/pyjsbuild
    and bin/pyjscompile?

    e.g. on Unix systems:

        python bootstrap.py /usr/share/pyjamas /usr
    """

    setup(name = "Pyjamas Desktop",
        version = version,
        description = "Pyjamas Widget API for Web applications, in Python",
        long_description = open('README', 'rt').read(),
        url = "http://pyj.be",
        author = "The Pyjamas Project",
        author_email = "lkcl@lkcl.net",
        keywords = keyw,
        packages=["pyjd"],
        package_dir = { 'pyjd': 'pyjd'},
        license = "Apache Software License",
        platforms = ["any"],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Natural Language :: English",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python"
        ])

