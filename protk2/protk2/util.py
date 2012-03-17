"""
protk2.util : ProTK utility functions
"""

import os,sys

def parse_args():
    # pull args from sys.argv
    args = sys.argv
    
    if len(args) > 1:
        args = args[1:]
        