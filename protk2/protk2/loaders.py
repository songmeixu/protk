'''
Created on Mar 16, 2012

@author: jacobokamoto
'''

from protk2.parsers import *
from protk2.db.types import AnalysisEntry, ProsodyEntry, AudioFile
from protk2.fs import *

def load_formant_sl(db_session, directory, file_ext="FormantSL"):
    files = list_file_paths(directory, include=file_ext)
    
    for f in files:
        af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
        if af.count() == 0:
            print("[loader][formantsl][load]> Ignoring file '%s' as it has no corresponding audio" % f)
        else: af = af[0]
        print("[loader][formantsl][load]> Loading formants from '%s'" % f)
        
        step = 0.00625
        formants = FormantSLParser(f).parse(af)
        numfmts = len(formants)
        duration = (step*numfmts)
        fmtvals = formants
        words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
        for word in words:
            s = word.start
            e = word.end
            start_index = int(s/step)
            end_index = int(e/step)
            
            for i in range(0,6):
                entries = [z[i][2] for z in fmtvals[start_index:end_index] if len(z) > i]
                if len(entries)!= 0:
                    ae = AnalysisEntry(entries, s, e, "f%d" % (i), word)
                    
                    #print "f%d:"%(i), ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index, duration
                
                    db_session.add(ae)
        db_session.commit()
        
def load_intensities(db_session, directory, file_ext="Intensity"):
    files = list_file_paths(directory, include=file_ext)
    
    for f in files:
        af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
        if af.count() == 0:
            print("[loader][analysis][intensity][load]> Ignoring intensity file at '%s' because it has no corresponding audio file" % f)
            continue
            
        else: af = af[0]
        print("[loader][analysis][intensity][load]> Loaded audio file record for '%s'" % af.filename)
        
        intensities = IntensityParser(f).parse()
        step = 0.008
        words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
        for word in words:
            s = word.start
            e = word.end
            start_index = int(s/step)
            end_index = int(e/step)
            
            entries = intensities[start_index:end_index]
            if len(entries) != 0:
                ae = AnalysisEntry(entries, s, e, "intensity", word)
                
                #print "intensity", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                
                db_session.add(ae)
        
        db_session.commit()
        
def load_shimmers(db_session, directory, file_ext="ShimmerLocal"):
    files = list_file_paths(directory, include=file_ext)

    print len(files)
    
    for f in files:
        af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
        if af.count() == 0:
            print("[loader][analysis][shimmerlocal][load]> Ignoring shimmer file at '%s' because it has no corresponding audio file" % f)
            continue
            
        else: af = af[0]
        print("[loader][analysis][shimmerlocal][load]> Loaded audio file record for '%s'" % af.filename)
        
        step = 0.02
        intensities = ShimmerParser(f).parse()
        words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
        for word in words:
            s = word.start
            e = word.end
            start_index = int(s/step)
            end_index = int(e/step)
            
            entries = [i[1] for i in intensities if i[0] > s and i[0] < e]
            if len(entries) != 0:
                ae = AnalysisEntry(entries, s, e, "shimmer", word)
                
                #print "shimmer", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                
                db_session.add(ae)
        
        db_session.commit()

def load_jitters(db_session, directory, file_ext="JitterLocal"): 
    files = list_file_paths(directory, include=file_ext)

    print len(files)
    
    for f in files:
        af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
        if af.count() == 0:
            print("[loader][analysis][jitterlocal][load]> Ignoring jitter file at '%s' because it has no corresponding audio file" % f)
            continue
            
        else: af = af[0]
        print("[loader][analysis][jitterlocal][load]> Loaded audio file record for '%s'" % af.filename)
        
        step = 0.02
        intensities = ShimmerParser(f).parse()
        words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
        for word in words:
            s = word.start
            e = word.end
            start_index = int(s/step)
            end_index = int(e/step)
            
            entries = [i[1] for i in intensities if i[0] > s and i[0] < e]
            if len(entries) != 0:
                ae = AnalysisEntry(entries, s, e, "jitter", word)
                
                #print "jitter", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                
                db_session.add(ae)
        
        db_session.commit()

def load_pitches(db_session, directory, file_ext="Pitch"):
    
    files = list_file_paths(directory, include=".Pitch")
    
    for f in files:
        af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
        if af.count() == 0:
            print("[loader][analysis][pitch][load]> Ignoring pitch file at '%s' because it has no corresponding audio file" % f)
            continue
            
        else: af = af[0]
        print("[loader][analysis][pitch][load]> Loaded audio file record for '%s'" % af.filename)
        
        step = 0.01
        intensities = PitchParser(f).parse()
        words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
        for word in words:
            s = word.start
            e = word.end
            start_index = int(s/step)
            end_index = int(e/step)
            
            entries = [i[1] for i in intensities if i[0] > s and i[0] < e]
            if len(entries) != 0:
                ae = AnalysisEntry(entries, s, e, "pitch", word)
                
                print "pitch", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                
                db_session.add(ae)
        
        db_session.commit()

def load_audio(db_session, directory, file_ext="wav"):
    
    if not dir_exists(directory): return False
    
    files = list_file_paths(directory, include=".wav")
    existing = [af.filename for af in db_session.query(AudioFile)]
    
    for f in files:
        if f not in existing:
            af = AudioFile(f)
            db_session.add(af)
            print("[loader][audio][load]> Loaded audio file with filename '%s'" % f)
        else:
            print("[loader][audio][load]> Audio file '%s' already exists in database. Ignoring." % f)
        
    db_session.commit()
    
def load_textgrids(db_session, directory, file_ext=["TextGrid","txtgrid"]):
    if not dir_exists(directory): return False
    
    files = list_file_paths(directory, include=".txtgrid")
    
    for f in files:
        af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
        if af.count() == 0:
            print("[loader][txtgrid][load]> Ignoring textgrid at '%s' because it has no corresponding audio file" % f)
            continue
        else: af = af[0]
        print "[loader][txtgrid][load]> Loaded audio file record for '%s' for textgrid '%s'" % (af.filename,f)
        contents = TextGridParser(f,af).parse()
        db_session.add_all(contents)
        db_session.commit()
        print("[loader][txtgrid][load]> Parsed textgrid file '%s' to database" % f)
