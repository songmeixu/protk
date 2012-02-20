'''
Created on Feb 9, 2012

ProTK v0.0.1-DEMONSTRATOR-DB

@author: jacobokamoto
'''

import sys
import os
from protk.db.types import *

pwd = os.environ["PWD"].strip() if os.environ.has_key("PWD") else "<unknown>"

PROTK_VERSION="0.0.1-DEMONSTRATOR-DB"

def usage():
    print """
ProTK v%s
""" % PROTK_VERSION

usage()