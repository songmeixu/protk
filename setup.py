#!/usr/bin/env python

from distutils.core import setup

install_dir="/usr/bin"

import os,sys

def parse_args():
    # pull args from sys.argv
    args = sys.argv
    
    if len(args) > 1:
        args = args[1:]
    else: return {}
    
    ret = {}
    
    for arg in args:
        if arg.find("=") != -1:
            parts = arg.split("=")
        else:
            parts = [arg]
            
        switch = parts[0]
        if switch.startswith("--"):
            if len(parts) > 1: ret[switch[2:]] = parts[1]
            else: ret[switch[2:]] = True
        else:
            print("Invalid option: %s" % switch)
            
    return ret

opts = parse_args()

if opts.has_key("tools-prefix"):
    install_dir=opts["prefix"]

setup(name='ProTK',
      version='0.3.0',
      description='Linguistic analysis toolkit',
      author='Jacob Okamoto',
      author_email='okam0013@umn.edu',
      url='https://github.com/oko/protk',
      packages=['protk2','protk2.db'],
      data_files=[(install_dir,['arff.py','ingest.py'])]
     )
