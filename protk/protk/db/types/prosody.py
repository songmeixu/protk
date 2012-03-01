'''
Created on Feb 17, 2012

@author: jacobokamoto
'''
import pickle
from sqlalchemy import Column,Float,Integer,String,ForeignKey,Text
from sqlalchemy.ext.declarative import declarative_base
from __init__ import get_metadata

Base = declarative_base()
Base.metadata = get_metadata()

class Word(Base):
    
    __tablename__ = "prosody_word"
    
    id = Column(Integer,primary_key=True)
    
    collection = Column(Integer,ForeignKey("prosody_collection.id"))
    
    start = Column(Float)
    end = Column(Float)
    
    word = Column(String(255))
    
    extdata = Column(Text)
    
    def __init__(self, prosody_collection, start, end, word, extdata):
        self.collection = prosody_collection.id
        self.start = start
        self.end = end
        self.word = word
        self.extdata = pickle.dumps(extdata)
        
    def __str__(self):
        return "<word:%s>" % self.word
    
class Phone(Base):
    
    __tablename__ = "prosody_phone"
    
    id = Column(Integer,primary_key=True)
    
    prosody_collection = Column(Integer,ForeignKey("prosody_collection.id"))
    
    start = Column(Float)
    end = Column(Float)
    
    phone = Column(String(255))
    
    extdata = Column(Text)

    def __init__(self, prosody_collection, start, end, phone, extdata):
        self.collection = prosody_collection.id
        self.start = start
        self.end = end
        self.phone = phone
        self.extdata = pickle.dumps(extdata)
        
    def __str__(self):
        return "<phone:%s>" % self.phone
    
def create_tables(engine):
    Base.metadata.create_all(engine)