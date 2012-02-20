'''
Created on Feb 18, 2012

@author: jacobokamoto
'''
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from protk.fs.directory import *
from protk.db.__init__ import DatabaseManager
from protk.db.types import analysis,prosody
from protk.script.engine import PraatScriptRunner
from protk.loaders.default import *

dbmgr = DatabaseManager({'driver':'sqlite3','name':'/home/jacobokamoto/testdata/sqlite.db'})
dbmgr.initialize_db([base_types,analysis,prosody])
session = dbmgr.get_session()

def usage():
    pass

if len(sys.argv) < 2:
    usage()
    exit(1)
    
args = sys.argv[1:]

audio_path = None
truth_path = None
train_path = None
script_path = None
praatoutput_path = None

while True:
    if len(args) == 0:
        break
    arg = args.pop(0)
    
    if arg == "--audio":
        audio_path = args.pop(0)
        if not os.path.exists(audio_path):
            print("[args][parse]> Invalid directory specified to '%s'" % arg)
            exit(1)
            
    elif arg == "--truth":
        truth_path = args.pop(0)
        if not os.path.exists(truth_path):
            print("[args][parse]> Invalid directory specified to '%s'" % arg)
            exit(1)
            
    elif arg == "--train":
        train_path = args.pop(0)
        if not os.path.exists(train_path):
            print("[args][parse]> Invalid directory specified to '%s'" % arg)
            exit(1)
            
    elif arg == "--script":
        script_path = args.pop(0)
        if not os.path.exists(script_path):
            print("[args][parse]> Invalid directory specified to '%s'" % arg)
            script_path = None
            
    elif arg == "--praatoutput":
        praatoutput_path = args.pop(0)
        if not os.path.exists(praatoutput_path):
            print("[args][parse]> Invalid directory specified to '%s'" % arg)
            praatoutput_path = None
            
    else:
        print("[args][parse]> Ignoring unknown option '%s'" % arg)
        
if audio_path == None or (train_path == None and truth_path == None):
    exit(2)
    
if script_path == None:
    script_path = normalize_dir_path(os.path.dirname(audio_path))+"script/"
if praatoutput_path == None:
    praatoutput_path = normalize_dir_path(os.path.dirname(audio_path))+"output/"
    
al = AudioLoader("/home/jacobokamoto/testdata/")
al.load(session)

tgl = TextGridLoader("/home/jacobokamoto/testdata/", CollectionTypes.Training)
tgl.load(session)

psr = PraatScriptRunner("/home/jacobokamoto/testdata/", "/home/jacobokamoto/testdata/script/", "/home/jacobokamoto/testdata/output/")
psr.generate_scripts()
psr.run_scripts()