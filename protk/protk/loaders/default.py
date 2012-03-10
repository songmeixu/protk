'''
Created on Feb 18, 2012

@author: jacobokamoto
'''
from protk.db import types as base_types
from protk.db.types import AudioFile,AnalysisCollection,ProsodyCollection,analysis,prosody,CollectionTypes
from protk.fs.directory import *
from protk.parsers.prosody.textgrid import TextGridParser

class AudioLoader(object):
    
    def __init__(self, directory):
        
        self.directory = normalize_dir_path(directory)
        
    def load(self, db_session):
        if not dir_exists(self.directory): return False
        
        files = list_file_paths(self.directory, include=".wav")
        existing = [af.filename for af in db_session.query(AudioFile)]
        
        for f in files:
            if f not in existing:
                af = AudioFile(f)
                db_session.add(af)
                print("[loader][audio][load]> Loaded audio file with filename '%s'" % f)
            else:
                print("[loader][audio][load]> Audio file '%s' already exists in database. Ignoring." % f)
            
        db_session.commit()
        
class TextGridLoader(object):
    
    def __init__(self, directory, collection_type):
        
        self.directory = normalize_dir_path(directory)
        self.collection_type = collection_type
        
    def load(self, db_session):
        if not dir_exists(self.directory): return False
        
        files = list_file_paths(self.directory, include=".txtgrid")
        
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][txtgrid][load]> Ignoring textgrid at '%s' because it has no corresponding audio file" % f)
                continue
            else: af = af[0]
            print "[loader][txtgrid][load]> Loaded audio file record for '%s' for textgrid '%s'" % (af.filename,f)
            exist_pc = db_session.query(ProsodyCollection).filter(ProsodyCollection.audio_file==af.id,ProsodyCollection.collection_type==self.collection_type)
            if exist_pc.count() != 0:
                print("[loader][txtgrid][load]> Collection of this type already exists. Ignoring.")
                continue
            pc = ProsodyCollection(af, self.collection_type)
            db_session.add(pc)
            db_session.commit()
            
            contents = TextGridParser(f, pc).parse()
            db_session.add_all(contents)
            db_session.commit()
            print("[loader][txtgrid][load]> Parsed textgrid file '%s' to database" % f)
            
            
from protk.db.types.prosody import ProsodyEntry
from protk.db.types.analysis import FormantBurg, FormantSL, AnalysisEntry
from protk.parsers.analysis.formant import FormantBurgParser, FormantSLParser
from protk.parsers.analysis.intensity import IntensityParser
from protk.parsers.analysis.shimmer import ShimmerLocalParser
from protk.parsers.analysis.pitch import PitchParser
 
class PraatAnalysisLoader(object):
    
    def __init__(self, directory):
        self.directory = directory
    
    def _load_formants(self, db_session):
        
        if not dir_exists(self.directory): return False
        
        files = list_file_paths(self.directory, include=".FormantBurg")
        """
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][analysis][formantburg][load]> Ignoring formant file at '%s' because it has no corresponding audio file" % f)
                continue
                
            else: af = af[0]
            print("[loader][analysis][formantburg][load]> Loaded audio file record for '%s'" % af.filename)
            
            exist_fb = db_session.query(FormantBurg).filter(FormantBurg.audio_file==af.id)
            if exist_fb.count() != 0:
                print("[loader][analysis][formantburg][load]> Formants already processed for this file. Ignoring")
                continue
            
            formants = FormantBurgParser(f).parse(af)
            db_session.add_all(formants)
            db_session.commit()
        """
        files = list_file_paths(self.directory, include=".FormantSL")
        
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][analysis][formantsl][load]> Ignoring formant file at '%s' because it has no corresponding audio file" % f)
                continue
                
            else: af = af[0]
            print("[loader][analysis][formantsl][load]> Loaded audio file record for '%s'" % af.filename)
            
            exist_fb = db_session.query(FormantSL).filter(FormantSL.audio_file==af.id)
            if exist_fb.count() != 0:
                print("[loader][analysis][formantsl][load]> Formants already processed for this file. Ignoring")
                continue
            
            formants = FormantSLParser(f).parse(af)
            numfmts = len(formants)
            duration = (0.00625*numfmts)
            fmtvals = formants
            words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
            for word in words:
                s = word.start
                e = word.end
                start_index = int(s/0.00625)
                end_index = int(e/0.00625)
                
                for i in range(0,6):
                    entries = [z[i][2] for z in fmtvals[start_index:end_index] if len(z) > i]
                    if len(entries)!= 0:
                        ae = AnalysisEntry(entries, s, e, "f%d" % (i), word)
                        
                        #print "f%d:"%(i), ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index, duration
                    
                        db_session.add(ae)
            db_session.commit()
            
        
        files = list_file_paths(self.directory, include=".Intensity")
        
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][analysis][intensity][load]> Ignoring intensity file at '%s' because it has no corresponding audio file" % f)
                continue
                
            else: af = af[0]
            print("[loader][analysis][intensity][load]> Loaded audio file record for '%s'" % af.filename)
            
            intensities = IntensityParser(f).parse()
            words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
            for word in words:
                s = word.start
                e = word.end
                start_index = int(s/0.008)
                end_index = int(e/0.008)
                
                entries = intensities[start_index:end_index]
                if len(entries) != 0:
                    ae = AnalysisEntry(entries, s, e, "intensity", word)
                    
                    #print "intensity", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                    
                    db_session.add(ae)
            
            db_session.commit()
        
        files = list_file_paths(self.directory, include=".ShimmerLocal")

        print len(files)
        
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][analysis][shimmerlocal][load]> Ignoring shimmer file at '%s' because it has no corresponding audio file" % f)
                continue
                
            else: af = af[0]
            print("[loader][analysis][shimmerlocal][load]> Loaded audio file record for '%s'" % af.filename)
            
            intensities = ShimmerLocalParser(f).parse()
            words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
            for word in words:
                s = word.start
                e = word.end
                start_index = int(s/0.02)
                end_index = int(e/0.02)
                
                entries = [i[1] for i in intensities if i[0] > s and i[0] < e]
                if len(entries) != 0:
                    ae = AnalysisEntry(entries, s, e, "shimmer", word)
                    
                    print "shimmer", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                    
                    db_session.add(ae)
            
            db_session.commit()
         
        files = list_file_paths(self.directory, include=".JitterLocal")

        print len(files)
        
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][analysis][shimmerlocal][load]> Ignoring shimmer file at '%s' because it has no corresponding audio file" % f)
                continue
                
            else: af = af[0]
            print("[loader][analysis][shimmerlocal][load]> Loaded audio file record for '%s'" % af.filename)
            
            intensities = ShimmerLocalParser(f).parse()
            words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
            print "loaded words"
            for word in words:
                s = word.start
                e = word.end
                start_index = int(s/0.02)
                end_index = int(e/0.02)
                
                entries = [i[1] for i in intensities if i[0] > s and i[0] < e]
                if len(entries) != 0:
                    ae = AnalysisEntry(entries, s, e, "jitter", word)
                    
                    print "jitter", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                    
                    db_session.add(ae)
            
            db_session.commit()

        files = list_file_paths(self.directory, include=".Pitch")
        
        for f in files:
            af = db_session.query(AudioFile).filter(AudioFile.basename==noext_name(f))
            if af.count() == 0:
                print("[loader][analysis][shimmerlocal][load]> Ignoring shimmer file at '%s' because it has no corresponding audio file" % f)
                continue
                
            else: af = af[0]
            print("[loader][analysis][shimmerlocal][load]> Loaded audio file record for '%s'" % af.filename)
            
            intensities = PitchParser(f).parse()
            words = db_session.query(ProsodyEntry).filter(ProsodyEntry.audio_file==af.id)
            for word in words:
                s = word.start
                e = word.end
                start_index = int(s/0.02)
                end_index = int(e/0.02)
                
                entries = [i[1] for i in intensities if i[0] > s and i[0] < e]
                if len(entries) != 0:
                    ae = AnalysisEntry(entries, s, e, "pitch", word)
                    
                    print "pitch", ae.mean, ae.median, ae.stdev, ae.slope, " / ", s, e, " / ", start_index, end_index
                    
                    db_session.add(ae)
            
            db_session.commit()
        

    def load(self, db_session):
        self._load_formants(db_session)
        
