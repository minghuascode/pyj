# Copyright (C) 2007-2008 The PyAMF Project.
# Copyright (C) 2009, 2014 Luke Kenneth Casson Leighton <lkcl@lkcl.net>
# See LICENSE for details.

import glob
from distutils.core import setup , run_setup

import sys
import os

version = os.environ.get('VERSION', open('VERSION', 'rt').read().strip())

keyw = """\
Pyjamas, GUI, Compiler, AJAX, Widget Set
"""

datadir = os.path.join("share", "pyjamas")

bp_data_files = glob.glob(os.path.join("builder", "boilerplate", "*"))
test_files = glob.glob(os.path.join("pyjs", "tests", "*"))
stub_files = glob.glob(os.path.join("stubs", "*"))
addons_data_files = glob.glob(os.path.join("addons", "*.py"))
#pygtkweb_data_files = glob.glob(os.path.join("pygtkweb", "*.py"))

data_files = [
    (os.path.join(datadir, "builder", "boilerplate"), bp_data_files),
    (os.path.join(datadir, "pyjs", "tests"), test_files),
    (os.path.join(datadir, "stubs"), stub_files),
    (os.path.join(datadir, "stubs"), stub_files),
    #(os.path.join(datadir, "pygtkweb"), pygtkweb_data_files)
]

# main purpose of this function is to exclude "output" which
# could have been built by a developer.
def get_files(d):
    res = []
    for p in glob.glob(os.path.join(d, "*")):
        if not p:
            continue
        (pth, fname) = os.path.split(p)
        if fname == "output":
            continue
        if fname == "PureMVC_Python_1_0":
            continue
        if fname[-4:] == ".pyc": # ehmm.. no.
            continue
        if os.path.isdir(p):
            get_dir(p)
        else:
            res.append(p)
    return res

def get_dir(dirname):
    for d in glob.glob("%s/*" % dirname):
        if os.path.isdir(d):
            (pth, fname) = os.path.split(d)
            expath = get_files(d)
            pth = os.path.join(os.path.join(datadir, dirname), fname)
            data_files.append((pth, expath))
        else:
            data_files.append((os.path.join(datadir, dirname), [d]))

# recursively grab the library and the examples subdirectories - all contents
get_dir("library")
get_dir("examples")

# likewise pyjs/src/pyjs
get_dir(os.path.join("pyjs", "src", "pyjs", "builtin"))
get_dir(os.path.join("pyjs", "src", "pyjs", "lib"))
get_dir(os.path.join("pyjs", "src", "pyjs", "boilerplate"))
get_dir(os.path.join("pgen"))

#from pprint import pprint
#pprint(data_files)

import distutils.core

if __name__ == '__main__':

    sys.stderr.write("""
    Have you run bootstrap.py to create bin/pyjsbuild
    and bin/pyjscompile?

    e.g. on Unix systems:

        python bootstrap.py /usr/share/pyjamas /usr
    """)

    setup(name = "Pyjamas",
        version = version,
        description = \
         "Pyjamas Widget API and Javascript compiler for Web apps, in Python",
        long_description = open('README', 'rt').read(),
        url = "http://pyj.be",
        author = "The Pyjamas Project",
        author_email = "lkcl@lkcl.net",
        keywords = keyw,
        packages=["pyjs", "pyjs.lib_trans",
                "pyjs.jsonrpc",
                "pyjs.jsonrpc.cgihandler",
                "pyjs.jsonrpc.mongrel2",
                "pyjs.jsonrpc.django",
                "pyjs.jsonrpc.web2py",
                "pyjs.jsonrpc.webpy",
                "pyjs.jsonrpc.bottle",
                "pyjs.jsonrpc.cherrypy",
                "pyjs.lib_trans",
                "pyjs.lib_trans.pycompiler",
                "pyjs.lib_trans.pyparser"],
        package_dir = {'pyjs': os.path.join('pyjs', 'src', 'pyjs'),
                       'pyjs.lib_trans':
                            os.path.join('pyjs', 'src', 'pyjs', 'lib_trans'),
                       'pyjs.lib_trans.pycompiler':
                            os.path.join('pyjs', 'src', 'pyjs',
                                         'lib_trans', 'pycompiler'),
                       'pyjs.lib_trans.pyparser':
                            os.path.join('pyjs', 'src', 'pyjs',
                                         'lib_trans', 'pyparser'),
                       'pyjs.jsonrpc': os.path.join('pyjs', 'jsonrpc'),
                       'pyjs.jsonrpc.cgihandler':
                                os.path.join('pyjs', 'jsonrpc', 'cgihandler'),
                       'pyjs.jsonrpc.mongrel2':
                                os.path.join('pyjs', 'jsonrpc', 'mongrel2'),
                       'pyjs.jsonrpc.django':
                                os.path.join('pyjs', 'jsonrpc', 'django'),
                       'pyjs.jsonrpc.cherrypy':
                                os.path.join('pyjs', 'jsonrpc', 'cherrypy'),
                       'pyjs.jsonrpc.bottle':
                                os.path.join('pyjs', 'jsonrpc', 'bottle'),
                       'pyjs.jsonrpc.webpy':
                                os.path.join('pyjs', 'jsonrpc', 'webpy'),
                       'pyjs.jsonrpc.web2py':
                                os.path.join('pyjs', 'jsonrpc', 'web2py'),
                       },
        data_files = data_files,
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

