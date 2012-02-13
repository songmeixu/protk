import os,sys

import core.db,core.fs,config
from core.db import DatabaseManager
from core.db.types import *
from core.util import get_arg_param

def usage():
    print """ProTK v%s""" % config.PROTK_VERSION
    print """-------"""+('-'*len(config.PROTK_VERSION))
    print
    print """Bulk Model Builder"""
    print """Usage:
    python build_bulk.py --truthdir=<directory> --traindir=<directory> --audiodir=<directory>
"""

TRUTH_DIR=None
TRAIN_DIR=None
AUDIO_DIR=None
TRUTH_FILES=None
TRAIN_FILES=None
AUDIO_FILES=None

if len(sys.argv) != 4:
    print sys.argv
    usage()
    exit(1)
else:
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith('--truthdir'):
            dirname = get_arg_param(arg)
            dirname = dirname[:-1] if dirname[-1] == '/' else dirname
            TRUTH_DIR=dirname
            print "[build]> Load truth files from %s" % dirname
            listing = None
            try:
                listing = core.fs.get_filenames(dirname)
            except:
                print "[build]> ERROR: Couldn't get files from truth directory"
                exit(1)
            TRUTH_FILES=[dirname+'/'+i for i in listing]
        elif arg.startswith('--traindir'):
            dirname = get_arg_param(arg)
            dirname = dirname[:-1] if dirname[-1] == '/' else dirname
            TRAIN_DIR=dirname
            print "[build]> Load training files from %s" % dirname
            listing = None
            try:
                listing = core.fs.get_filenames(dirname)
            except:
                print "[build]> ERROR: Couldn't get files from training directory"
                exit(1)
            TRAIN_FILES=[dirname+'/'+i for i in listing]
        elif arg.startswith('--audiodir'):
            dirname = get_arg_param(arg)
            dirname = dirname[:-1] if dirname[-1] == '/' else dirname
            AUDIO_DIR=dirname
            print "[build]> Load audio files from %s" % dirname
            listing = None
            try:
                listing = core.fs.get_filenames(dirname)
            except:
                print "[build]> ERROR: Couldn't get files from audio directory"
                exit(1)
            AUDIO_FILES=[dirname+'/'+i for i in listing]
        else:
            print "[build]> ERROR: Invalid argument '%s' -- exiting" % arg
            exit(1)

