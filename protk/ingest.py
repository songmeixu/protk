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
noexec = False

while True:
    if len(args) == 0:
        break
    arg = args.pop(0)
    print arg
     
    if arg == "--audio":
        audio_path = normalize_dir_path(args.pop(0))
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
    elif arg == "--noexec":
        noexec = True
        print("[args][parse]> --noexec : WILL NOT EXECUTE PRAAT SCRIPTS ON THIS RUN")
    
    else:
        print("[args][parse]> Ignoring unknown option '%s'" % arg)
        
if audio_path == None or (train_path == None and truth_path == None):
    exit(2)


dbmgr = DatabaseManager({'driver':'sqlite3','name':audio_path+'sqlite.db'})
dbmgr.initialize_db([base_types,analysis,prosody])
session = dbmgr.get_session()
    
if script_path == None:
    script_path = normalize_dir_path(os.path.dirname(audio_path))+"script/"
if praatoutput_path == None:
    praatoutput_path = normalize_dir_path(os.path.dirname(audio_path))+"output/"
    
al = AudioLoader(audio_path)
al.load(session)

tgl_train = None
if train_path != None:
    tgl_train = TextGridLoader(train_path, CollectionTypes.Training)
    tgl_train.load(session)

tgl_truth = None
if truth_path != None:
    tgl_truth = TextGridLoader(truth_path, CollectionTypes.Truth)
    tgl_truth.load(session)
if not noexec:
    psr = PraatScriptRunner(audio_path, script_path, praatoutput_path)
    psr.generate_scripts()
    psr.run_scripts()

pal = PraatAnalysisLoader(praatoutput_path)
pal.load(session)
