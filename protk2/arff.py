"""
arff.py : ARFF output script for ProTK 2
"""

import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from protk2.db.core import *
from protk2.db.types import *
from protk2.loaders import *
from protk2.parsers import *
from protk2.fs import *
from protk2.praat import *
from protk2.util import *
from protk2.arff import *

opts = parse_args()
from config import CONFIG

dbconf = CONFIG["database"]
db = DatabaseManager(dbconf)
create_tables(db.engine)
db_session = db.get_session()

entries = None

if opts.has_key("type"):
    entries = db_session.query(ProsodyEntry).filter(ProsodyEntry.ptype==opts["type"])
else:
    entries = db_session.query(ProsodyEntry)
    
attributes = [("duration","NUMERIC"),
              ("pitch","NUMERIC"),
              ("intensity","NUMERIC"),
              ("f1","NUMERIC"),
              ("f2","NUMERIC"),
              #("shimmer","NUMERIC"),
              #("jitter","NUMERIC"),
              #("word","STRING"),
              ("truth","{YES,NO}"),]

allvals = []

if opts.has_key("searchtier") and opts.has_key("searchfor"):
    search = db_session.query(ProsodyEntry).filter(ProsodyEntry.ptype==opts["searchtier"]).filter(ProsodyEntry.data==opts["searchfor"])
else:
    search = False

for entry in entries:
    features = db_session.query(AnalysisEntry).filter(AnalysisEntry.prosody_entry==entry.id)
    if features.count() == 0:
        #print("No features.")
        continue
    #else:
        #print("%d features."%features.count())
    fd = {}
    for f in features:
        fd[f.atype] = f
    fd["duration"] = entry.end - entry.start
    #sfd["word"] = entry.data
    if not search:
        fd["truth"] = "YES" if entry.data == "FILLEDPAUSE_um" else "NO"
    else:
        for s in search:
            #print s.start, entry.start, entry.end, s.end, s.start-0.1 <= entry.start and s.end+0.1 >= entry.end
            
            if s.start-0.1 <= entry.start and s.end+0.1 >= entry.end:
                fd["truth"] = "YES"
                break
        if not fd.has_key("truth"): fd["truth"] = "NO"
    if not has_keys(fd,[i[0] for i in attributes]): 
        #print("This attribute (id:%d) was not extracted for this element. Skipping." % entry.id)
        pass
    else:
        vals = []
        for attr in [i[0] for i in attributes]:
            x = fd[attr]
            if type(x) is AnalysisEntry:
                x = x.mean
            vals.append(x)
        allvals.append(vals)
        
output = generate_arff("langmodel", attributes, allvals)
for o in output:
    print o