#!/usr/bin/env python
"""
ingest.py : Data ingest script for ProTK 2
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

opts = parse_args()
from config import CONFIG

dbconf = CONFIG["database"]
db = DatabaseManager(dbconf)
create_tables(db.engine)
db_session = db.get_session()

if not opts.has_key("audio"):
    print("ERROR> Audio directory does not exist")
    exit(2)

audio_dir = normalize_dir_path(opts["audio"])
load_audio(db_session, audio_dir)

if opts.has_key("framesize"):
    window_size = None
    frame_size = float(opts["framesize"])
    if opts.has_key("windowsize"): window_size = float(opts["windowsize"])
    
    afs = db_session.query(AudioFile)
    
    for af in afs:
        generate_framing(frame_size, window_size, db_session, af)
        
if opts.has_key("textgrid"):
    txtgrd_dir = opts["textgrid"]
    load_textgrids(db_session, txtgrd_dir)

print audio_dir

script_dir = audio_dir+"script/"
output_dir = audio_dir+"output/"

if opts.has_key("scriptdir"):
    script_dir = normalize_dir_path(opts["scriptdir"])
if opts.has_key("outputdir"):
    output_dir = normalize_dir_path(opts["outputdir"])

if opts.has_key("praat"):
    
    psr = PraatScriptRunner(audio_dir, script_dir, output_dir)
    psr.generate_scripts()
    psr.run_scripts()
    
if opts.has_key("formants"):
    load_formant_sl(db_session, output_dir)
    
if opts.has_key("shimmer"):
    load_shimmers(db_session, output_dir)
    
if opts.has_key("jitter"):
    load_jitters(db_session, output_dir)
    
if opts.has_key("intensities"):
    load_intensities(db_session, output_dir)
    
if opts.has_key("pitches"):
    load_pitches(db_session, output_dir)
