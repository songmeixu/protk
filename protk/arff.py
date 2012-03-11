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
#for af in afs:

print "@RELATION wordfeatures"
print
print "@ATTRIBUTE   duration    numeric"
print "@ATTRIBUTE   pitch       numeric"
print "@ATTRIBUTE   intensity   numeric"
print "@ATTRIBUTE   f1          numeric"
print "@ATTRIBUTE   f2          numeric"
print "@ATTRIBUTE   shimmer     numeric"
print "@ATTRIBUTE   jitter      numeric"
print "@ATTRIBUTE   truth       string"
print 
print "@DATA"

words = session.query(ProsodyEntry).filter(ProsodyEntry.ptype=="word")
for w in words:
    features = session.query(AnalysisEntry).filter(AnalysisEntry.prosody_entry==w.id)
    if features.count() == 0:
        continue
    else:
        fd = {}
        for f in features:
            fd[f.atype] = f

        if not fd.has_key("pitch") or not fd.has_key("intensity") or not fd.has_key("f1") or not fd.has_key("f2") or not fd.has_key("shimmer") or not fd.has_key("jitter"):
            continue

        print "%f,%f,%f,%f,%f,%f,%f,%s"%((w.end-w.start),fd["pitch"].mean,fd["intensity"].mean,fd["f1"].mean,fd["f2"].mean,fd["shimmer"].mean,fd["jitter"].mean,("YES" if w.data == "FILLEDPAUSE_um" or w.data == "FILLEDPAUSE_ah" else "NO"))
