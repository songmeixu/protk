#!/usr/bin/env python
"""
arff.py : ARFF output script for ProTK 2
"""

import os,sys
from numpy.ctypeslib import ct
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from protk2.db.core import *
from protk2.db.types import *
from protk2.loaders import *
from protk2.parsers import *
from protk2.fs import *
from protk2.praat import *
from protk2.util import *
from protk2.arff import *
from protk2.config import *

opts = parse_args()

CONFIG = None

if opts.has_key("config"):
    if os.path.exists(opts["config"]):
        execfile(opts["config"])
else:
    from protk2.config import *

db = DatabaseManager(DATABASE)
create_tables(db.engine)
db_session = db.get_session()

entries = None

if opts.has_key("type"):
    entries = list(db_session.query(ProsodyEntry).filter(ProsodyEntry.ptype==opts["type"]))
else:
    entries = list(db_session.query(ProsodyEntry))
    

if opts.has_key("searchtier") and opts.has_key("searchfor"):
    sf = opts['searchfor'].split(',')
    base_q = """db_session.query(ProsodyEntry).filter(ProsodyEntry.ptype==opts["searchtier"])"""
    for s in sf:
        base_q = base_q + """.filter(ProsodyEntry.data=="%s")"""%s
    search = eval(base_q)
else:
    search = False

targets = ["filledpause_um","filledpause_ah"]
if opts.has_key("targets"):
    targets = opts["targets"].lower().split(",")

idx=0
for entry in entries:
    entry.features = {}
    fs = db_session.query(AnalysisEntry).filter(AnalysisEntry.prosody_entry==entry.id)
    for f in fs:
        entry.features[f.atype] = f

context_size=ARFF_CONTEXT_SIZE
if opts.has_key("context"):
    context_size = int(opts["context"])
   
   
# THIS IS OLD CODE FOR DEVELOPMENT REFERENCE ONLY 
"""
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
    if a[1] == "NUMERIC" and a[0].find("duration") == -1:
        for s in subattributes:
            newattr.append((a[0]+"_"+s,"NUMERIC"))
    else:
        newattr.append(a)
        
#print newattr

allvals = []
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
            if entry.data.lower() == target:
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
"""

entry_rows = []

idx = 0
for i in range(len(entries)):
    ctx_entries = [None]*(context_size*2+1)
    if i < context_size:
        for z in range((context_size-i)):
            ctx_entries[i+z] = entries[0]
    for z in range(context_size):
        z=z+1
        l = -z
        r = z
        if l <= 0:
            ctx_entries[context_size+l] = entries[i-z]
        if i+r < len(entries):
            ctx_entries[context_size+r] = entries[i+z]
            
    ctx_entries[context_size] = entries[i]        
    entry_rows.append(ctx_entries)
    
def build_element(element,conf):
    output = []
    for feature_type,attributes in conf.iteritems():
        if element.features.has_key(feature_type):
            feat = element.features[feature_type]
            for a in attributes:
                if hasattr(feat,a) and feat.undefined != 1:
                    output.append(eval("feat."+a))
        else:
            output = output+(["?"]*len(attributes))
    return output
    
arff_rows = []
    
for r in range(len(entry_rows)):
    row = []
    for ele in entry_rows[r]:
        if ele != None:
            row = row + build_element(ele,ARFF_FEATURES)
    
    if ARFF_SHOW_WORD and entries[r] != None: row.append(entries[r].data.strip(""" \t"',.""").replace("'","_") if entries[r].data != "" else "BLANK")
    
    if entries[r] != None:
        if not search:
            y = False
            for t in targets:
                if t.lower() == entries[r].data.lower():
                    y = True
                    break
            if y: row.append("YES")
            else: row.append("NO")
        else:
            middle = (entries[r].start+entries[r].end)/2
            y = False
            for s in search:
                y = False
                if middle >= s.start and middle <= s.end:
                    print s.start,middle,s.end
                    y = True
                    break
            if y: row.append("YES")
            else: row.append("NO")
    
    arff_rows.append(row)

# Build attribute list
attributes = []
for i in range(context_size*2+1):
    for feat,attrs in ARFF_FEATURES.iteritems():
        for attr in attrs:
            attributes.append(("ctx%d_%s_%s"%(i,feat,attr),"NUMERIC"))
            
if ARFF_SHOW_WORD: attributes.append(("word","STRING"))
attributes.append(("truth","{YES,NO}"))

al = len(attributes)
for r in arff_rows:
    if len(r) != al:
        print len(r)

output = generate_arff("langmodel", attributes, arff_rows)

f = open("output.arff","w")

f.writelines([i+"\n" for i in output])