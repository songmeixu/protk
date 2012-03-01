'''
Created on Mar 1, 2012

@author: jacobokamoto
'''
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from protk.fs.directory import *
from protk.db.__init__ import DatabaseManager
from protk.db.types import analysis,prosody
from protk.db.types import ProsodyCollection
from protk.script.engine import PraatScriptRunner
from protk.loaders.default import *
from protk.db.types.analysis import FormantBurg, FormantSL
from protk.db.types.prosody import Word, Phone

def usage():
    print "<<USAGE>>"
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
    print("No audio path. Exiting.")
    exit(2)


dbmgr = DatabaseManager({'driver':'sqlite3','name':audio_path+'sqlite.db'})
dbmgr.initialize_db([base_types,analysis,prosody])
session = dbmgr.get_session()

print "derp"

cs = session.query(ProsodyCollection)
for c in cs:
    print "\n\n\n"
    words = session.query(Word).filter(Word.collection == c.id)
    for word in words:
        formants = session.query(FormantBurg).filter(FormantBurg.xmin >= word.start).filter(FormantBurg.xmax <= word.end).filter(FormantBurg.audio_file == c.audio_file)
        s = 0.0
        for f in formants:
            s += f.f1_o_f2()
        s = s / formants.count()
        print word.word, word.start, word.end, s
        #for f in formants: print f.audio_file, c.audio_file
