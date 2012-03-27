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
import pickle

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

excludes = []
if opts.has_key("exclude"):
    excludes = opts["exclude"].lower().split(',')

passthrough = []
if opts.has_key("passthrough"):
    passthrough = [i.split(":") for i in opts["passthrough"].split(',')]

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

import base64
    
for r in range(len(entry_rows)):
    row = []
    for ele in entry_rows[r]:
        if ele != None:
            row = row + build_element(ele,ARFF_FEATURES)
    
    if ARFF_SHOW_WORD and entries[r] != None: row.append(entries[r].data.strip(""" \t"',.""").replace("'","_") if entries[r].data != "" else "BLANK")

    if len(passthrough) != 0:
        for pt in passthrough:
            pt = pt[0]
            if entries[r].extdata != None and entries[r].extdata != "":
            #    try:
                    if pickle.loads(unicode(entries[r].extdata)).has_key(pt):
                        row.append(pickle.loads(unicode(entries[r].extdata))[pt])
                    else:
                        row.append("?")
            #    except:
                    #row.append("?")
            else:
                row.append("?")
    
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
    
    if entries[r].data.lower() not in excludes:
        arff_rows.append(row)

if len(excludes) != 0:
    print("Excluded %d items from ARFF out of total %d items (%f%%)"%(len(entries)-len(arff_rows),len(entries),1.0-float(len(arff_rows))/float(len(entries))))

# Build attribute list
attributes = []
for i in range(context_size*2+1):
    for feat,attrs in ARFF_FEATURES.iteritems():
        for attr in attrs:
            attributes.append(("ctx%d_%s_%s"%(i,feat,attr),"NUMERIC"))
            
if ARFF_SHOW_WORD: attributes.append(("word","STRING"))
if len(passthrough) != 0:
    for pt in passthrough:
        attributes.append((pt[0],pt[1]))

attributes.append(("truth","{YES,NO}"))

al = len(attributes)
for r in arff_rows:
    if len(r) != al:
        print len(r)

output = generate_arff("langmodel", attributes, arff_rows)

f = open("output.arff","w")

f.writelines([i+"\n" for i in output])
