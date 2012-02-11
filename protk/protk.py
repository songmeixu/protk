'''
Created on Feb 9, 2012

ProTK v0.0.1-DEMONSTRATOR-DB

@author: jacobokamoto
'''

import sys
import os
from core.db.types import *

pwd = os.environ["PWD"].strip() if os.environ.has_key("PWD") else "<unknown>"

PROTK_VERSION="0.0.1-DEMONSTRATOR-DB"

def usage():
    print """
ProTK v%s

Usage:
    --truth    [filename]  
""" % PROTK_VERSION

OPTIONS = {}

skip_arg = False
for i in range(len(sys.argv)):
    
    if skip_arg:
        skip_arg = False
        continue
    
    if i == 0:
        print "Running ProTK from file %s in %s" % (sys.argv[0],pwd)
        continue
    
    arg = sys.argv[i]
    narg = sys.argv[i+1] if i + 1 < len(sys.argv) else None
    
    if arg == "--truth":
        print "> Input file chosen using --truth: %s" % narg
        if not os.path.exists(narg):
            print "> ERROR[protk]: Input file does not exist"
            exit(1)
        OPTIONS["truth"] = narg
        skip_arg = True
    elif arg == "--truthdir":
        print "> Input directory chosen using --truthdir: %s" % narg
        if not os.path.exists(narg):
            print "> ERROR[protk]: Input directory does not exist"
            exit(1)
        try:
            contents = os.listdir(narg)
            OPTIONS["truth"] = contents
        except:
            print "> ERROR[protk]: Couldn't list contents of directory"
            exit(1)
        skip_arg = True
            
    elif arg == "-h" or arg == "--help":
        usage()
        exit(0)
    
    else:
        if arg[0:2] == "--":
            print "> WARN[protk]: Unknown option '%s'" % arg
        else:
            print "> WARN[protk]: Unknown/orphaned argument '%s'" % arg

from praat.textgrid import TextGrid        
import core.db

import config

session = core.db.get_session(config.DATABASE)

if OPTIONS.has_key("truth"):
    if type(OPTIONS["truth"]) is str:
        tg = TextGrid(OPTIONS["truth"])
        tg.add_to_db(session,truth=True)
else:
    core.db.dump_data(session)


