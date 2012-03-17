"""
protk2.db.types : Database types for ProTK 2
"""

from sqlalchemy.ext.declarative import declarative_base
import pickle
from sqlalchemy import Column,Float,Integer,String,ForeignKey,Text
from protk.fs.directory import noext_name

Base = declarative_base()

class AudioFile(Base):
    __tablename__ = "audio_file"
    
    id = Column(Integer,primary_key=True)
    
    filename = Column(String(255))
    basename = Column(String(255))
    
    extdata = Column(Text)
    
    def __init__(self, filename, extdata=None):
        self.filename = filename
        self.basename = noext_name(filename)
        self.extdata = pickle.dumps(extdata) if extdata != None else None

"""
ProsodyEntry: Holds information about a specific prosodic event (i.e., word, phoneme, phrase)
"""
class ProsodyEntry(Base):
    
    __tablename__ = "prosody_entries"
    
    id = Column(Integer,primary_key=True)
    
    audio_file = Column(Integer,ForeignKey("audio_file.id"))
    
    ptype = Column(String(255))
    
    start = Column(Float)
    end = Column(Float)
    
    data = Column(String(255))
    
    extdata = Column(Text)
    
    def __init__(self, audio_file, start, end, ptype, data, extdata):
        self.audio_file = audio_file.id
        self.start = start
        self.end = end
        self.data = str(data)
        self.extdata = pickle.dumps(extdata)
        self.ptype = ptype
        
    def __str__(self):
        return "<word:%s>" % self.word

import numpy
import numpy.linalg

"""
AnalysisEntry: Holds analysis results for a specific prosodic event
"""
class AnalysisEntry(Base):
    __tablename__ = "analysis_entries"
    
    id = Column(Integer,primary_key=True)
    
    prosody_entry = Column(Integer, ForeignKey("prosody_entries.id"))
    
    atype = Column(String(255))
    
    median = Column(Float)
    mean = Column(Float)
    stdev = Column(Float)
    slope = Column(Float)
    maxval = Column(Float)
    minval = Column(Float)
    
    def __init__(self, values, xmin, xmax, atype, prosody_entry, times=None):
        valarr = numpy.array(values)
        rngarr = numpy.arange(len(valarr))
        
        self.mean = float(numpy.mean(valarr))
        self.median = float(numpy.median(valarr))
        self.stdev = float(numpy.std(valarr))
        self.minval = float(numpy.nanmin(valarr))
        self.maxval = float(numpy.nanmax(valarr))
        #self.slope = (float(numpy.mean(numpy.array(values[-11:-1]))) - float(numpy.mean(numpy.array(values[0:10])))) / (xmax-xmin)
        slp = numpy.polyfit(rngarr, valarr, 1, full=False)
        self.slope = float(slp[0])
        self.prosody_entry = prosody_entry.id
        self.atype = atype