'''
Created on Mar 8, 2012

@author: jacobokamoto
'''
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from protk.db.__init__ import DatabaseManager,AudioFile
import protk.db.__init__ as base_types
from protk.db.types import prosody,analysis
from protk.db.types.analysis import AnalysisEntry
from protk.db.types.prosody import ProsodyEntry
from protk.fs.directory import *

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
    else:
        print("[args][parse]> Ignoring unknown option '%s'" % arg)
        
if audio_path == None:
    exit(2)

dbmgr = DatabaseManager({'driver':'sqlite3','name':audio_path+'sqlite.db'})
dbmgr.initialize_db([base_types,analysis,prosody])
session = dbmgr.get_session()

afs = session.query(AudioFile)
for af in afs:
    print af.filename
    words = session.query(ProsodyEntry).filter(ProsodyEntry.ptype=="word").filter(ProsodyEntry.audio_file==af.id)
    for w in words:
        features = session.query(AnalysisEntry).filter(AnalysisEntry.prosody_entry==w.id)
        print w.data
        for f in features:
            print f.atype, f.mean, f.median