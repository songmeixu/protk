"""
protk2.util : ProTK utility functions
"""

import os,sys

def parse_args():
    # pull args from sys.argv
    args = sys.argv
    
    if len(args) > 1:
        args = args[1:]
    else: return {}
    
    ret = {}
    
    for arg in args:
        if arg.find("=") != -1:
            parts = arg.split("=")
        else:
            parts = [arg]
            
        switch = parts[0]
        if switch.startswith("--"):
            if len(parts) > 1: ret[switch[2:]] = parts[1]
            else: ret[switch[2:]] = True
        else:
            print("Invalid option: %s" % switch)
            
    return ret

def merge_options(defaults, overrides):
    
    for k,v in overrides.iteritems():
        defaults[k] = v
        
    return defaults

from protk2.db.types import ProsodyEntry

def generate_framing(frame_size, window_size, db_session, audio_file):
    
    import wave
    import contextlib
    fname=audio_file.filename
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames=f.getnframes()
        rate=f.getframerate()
        duration=frames/float(rate)
        print duration

    if window_size == None: window_size = 0
    
    x = 0.0
    while x < duration:
        # set xmin/xmax
        xmin = x
        xmax = x + frame_size + window_size
        
        # add entry to database
        db_session.add(ProsodyEntry(audio_file, xmin, xmax, "frame", "", None))
        
        # advance x pointer
        x = x + frame_size
        
def has_keys(d,keys):
    for k in keys:
        if not d.has_key(k):
            print str(k)
            return False
    return True