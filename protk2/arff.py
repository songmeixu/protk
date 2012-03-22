#!/usr/bin/env python
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
from protk2.config import CONFIG

dbconf = CONFIG["database"]
db = DatabaseManager(dbconf)
create_tables(db.engine)
db_session = db.get_session()

entries = None

if opts.has_key("type"):
    entries = list(db_session.query(ProsodyEntry).filter(ProsodyEntry.ptype==opts["type"]))
else:
    entries = list(db_session.query(ProsodyEntry))
    
attributes = [("ctxb_duration","NUMERIC"),
              ("ctxb_pitch","NUMERIC"),
              ("ctxb_f1","NUMERIC"),
              ("ctxb_f2","NUMERIC"),
              ("duration","NUMERIC"),
              ("pitch","NUMERIC"),
              ("f1","NUMERIC"),
              ("f2","NUMERIC"),
              ("ctxa_duration","NUMERIC"),
              ("ctxa_pitch","NUMERIC"),
              ("ctxa_f1","NUMERIC"),
              ("ctxa_f2","NUMERIC"),
              #("shimmer","NUMERIC"),
              #("jitter","NUMERIC"),
              ("word","STRING"),
              ("truth","{YES,NO}"),]

subattributes = ["mean","median","stdev","minval","maxval","slope"]

newattr = []

for a in attributes:
    if a[1] == "NUMERIC":
        for s in subattributes:
            newattr.append((a[0]+"_"+s,"NUMERIC"))
        
print newattr

allvals = []

if opts.has_key("searchtier") and opts.has_key("searchfor"):
    search = db_session.query(ProsodyEntry).filter(ProsodyEntry.ptype==opts["searchtier"]).filter(ProsodyEntry.data==opts["searchfor"])
else:
    search = False

targets = ["filledpause_um","filledpause_ah"]
if opts.has_key("targets"):
    targets = opts["targets"].split(",")

idx=0
for entry in entries:
    entry.features = db_session.query(AnalysisEntry).filter(AnalysisEntry.prosody_entry==entry.id)

context_size=1
if opts.has_key("context"):
    context_size = int(opts["context"])

idx = 0
for entry in entries:
    if entry.features.count() == 0:
        #print("No features.")
        continue
    #else:
        #print("%d features."%features.count())
    fd = {}
    for f in entry.features:
        fd[f.atype] = f
        
    entry = entries[idx]
    if idx > 0:
        entry_b = entries[idx-1]
    else: entry_b = entry
    if idx+1 < len(entries):
        entry_a = entries[idx+1]
    else: entry_a = entry
    
    for f in entry_b.features:
        fd["ctxb_"+f.atype] = f
    for f in entry_a.features:
        fd["ctxa_"+f.atype] = f
    
    fd["duration"] = entry.end - entry.start
    fd["ctxb_duration"] = entry_b.end - entry_b.start
    fd["ctxa_duration"] = entry_a.end - entry_a.start
    fd["word"] = entry.data
    if not fd.has_key("shimmer"): fd["shimmer"] = "?"
    if not fd.has_key("jitter"): fd["jitter"] = "?"   
    
    if not search:
        found = False
        for target in targets:
            if entry.data == target:
                found = True
        fd["truth"] = "YES" if found else "NO"
    else:
        for s in search:
            #print s.start, entry.start, entry.end, s.end, s.start-0.1 <= entry.start and s.end+0.1 >= entry.end
            
            if s.start-0.1 <= entry.start and s.end+0.1 >= entry.end and s.audio_file == entry.audio_file:
                fd["truth"] = "YES"
                break
        if not fd.has_key("truth"): fd["truth"] = "NO"
    if not has_keys(fd,[i[0] for i in attributes]): 
        print("This attribute (id:%d) was not extracted for this element. Skipping." % entry.id)
        pass
    else:
        vals = []
        for attr in [i[0] for i in attributes]:
            x = fd[attr]
            if type(x) is AnalysisEntry:
                #x = x.mean if x.undefined == 0 else "?"
                for s in subattributes:
                    vals.append(eval("x."+s))
            else:
                vals.append(x)
        allvals.append(vals)
        
    idx = idx+1
        
output = generate_arff("langmodel", attributes, allvals)

f = open("output.arff","w")

f.writelines([i+"\n" for i in output])