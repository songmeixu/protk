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

class CollectionTypes:
    Truth = 1
    Training = 2
    Passthrough = 3

class ProsodyCollection(Base):
    __tablename__ = "prosody_collection"
    
    id = Column(Integer,primary_key=True)
    
    audio_file = Column(Integer,ForeignKey(AudioFile.__tablename__+".id"))
    
    collection_type = Column(Integer)
    
    def __init__(self,audio_file,collection_type):
        self.audio_file = audio_file.id
        self.collection_type = collection_type
    
class AnalysisCollection(Base):
    __tablename__ = "analysis_collection"
    
    id = Column(Integer,primary_key=True)
    
    audio_file = Column(Integer,ForeignKey(AudioFile.__tablename__+".id"))
    
    collection_type = Column(Integer)
    
    def __init__(self,audio_file,collection_type):
        self.audio_file = audio_file.id
        self.collection_type = collection_type

def create_tables(engine):
    Base.metadata.create_all(engine)
    
def get_metadata():
    return Base.metadata