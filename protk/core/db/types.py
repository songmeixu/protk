import os
PROTK_DEBUG=False
if os.environ.has_key("PROTK_DEBUG"):
    PROTK_DEBUG = True

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, UniqueConstraint

Base = declarative_base()

import sndhdr
import pickle

class AudioFile(Base):
    
    __tablename__ = 'audio_file'

    id = Column(Integer, primary_key=True)

    filename = Column(Text)
    filedata = Column(Text)
    duration = Column(Float)
    
    def __init__(self, filename):
        self.filename = filename
        try:
            filedata = sndhdr.whathdr(filename)
            sr = filedata[1]
            fr = filedata[3]
    
            self.duration = float(fr) / float(sr)
            self.filedata = pickle.dumps(filedata)
            
            if PROTK_DEBUG:
                print("DEBUG[db.types.AudioFile]> Audio file processed")
                print("DEBUG[db.types.AudioFile]>  - File type: %s" % filedata[0])
                print("DEBUG[db.types.AudioFile]>  - Sample rate: %s" % filedata[1])
            
        except Exception:
            raise Exception("Sound file could not be processed. This may be because the file does not exist.")
    def get_filedata(self):
        return pickle.loads(self.filedata)
    
class ProsodyCollection(Base):
    
    class Types:
        Truth = 0
        Training = 1
    
    __tablename__ = 'prosody_collection'
    
    __table_args__ = (UniqueConstraint('audio_file','collection_type'),)
    
    id = Column(Integer, primary_key=True)

    audio_file = Column(Integer, ForeignKey('audio_file.id'))
    
    collection_type = Column(Integer)
    
    extdata = Column(Text)

    def __init__(self, audio_file, truth=False, extdata=None):
        self.audio_file = audio_file.id
        self.extdata = pickle.dumps(extdata)
        if truth:
            self.collection_type = ProsodyCollection.Types.Truth
        else:
            self.collection_type = ProsodyCollection.Types.Training

class ProsodyTier(Base):
    
    __tablename__ = 'prosody_tier'

    id = Column(Integer, primary_key=True)

    collection = Column(Integer, ForeignKey('prosody_collection.id'))

    tier_type = Column(String(255))

    extdata = Column(Text)

    def __init__(self, collection, tier_type, extdata=None):
        self.collection = collection.id
        self.tier_type = tier_type
        self.extdata = pickle.dumps(extdata)

class ProsodyData(Base):
    
    __tablename__ = 'prosody_data'

    id = Column(Integer, primary_key=True)

    tier = Column(Integer, ForeignKey('prosody_tier.id'))

    xmin = Column(Float)
    xmax = Column(Float)

    duration = Column(Float)

    value = Column(String(255))

    extdata = Column(Text)

    def __init__(self, tier, xmin, xmax, value, extdata=None):
        self.tier = tier.id
        self.xmin = xmin
        self.xmax = xmax
        self.duration = self.xmax - self.xmin
        self.value = str(value)
        self.extdata = pickle.dumps(extdata)
    

class AnalysisCollection(Base):
    
    __tablename__ = 'analysis_collection'

    id = Column(Integer, primary_key=True)

    audio_file = Column(Integer, ForeignKey('audio_file.id'))

    extdata = Column(Text)

class AnalysisTier(Base):
    
    __tablename__ = 'analysis_tier'

    id = Column(Integer, primary_key=True)
    
    collection = Column(Integer, ForeignKey('analysis_collection.id'))

    tier_type = Column(String(255))

    frame_count = Column(Integer)
    frame_size = Column(Float)

    def __init__(self, collection, tier_type, frame_count, frame_size):
        self.collection = collection.id
        self.tier_type = tier_type
        self.frame_count = frame_count
        self.frame_size = frame_size

class AnalysisData(Base):
    
    __tablename__ = 'analysis_data'

    id = Column(Integer, primary_key=True)

    tier = Column(Integer, ForeignKey('analysis_tier.id'))

    value = Column(Float)
    xmin = Column(Float)
    xmax = Column(Float)

    def __init__(self, tier, value, xmin=None, xmax=None):
        self.tier = tier.id
        self.value = value
        self.xmin = xmin
        self.xmax = xmax
