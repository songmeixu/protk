'''
Created on Feb 17, 2012

@author: jacobokamoto
'''

from sqlalchemy import Column,Float,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from __init__ import get_metadata

Base = declarative_base()
Base.metadata = get_metadata()

class FormantBurg(Base):
    __tablename__ = "analysis_formant_burg"
    
    id = Column(Integer,primary_key=True)
    
    audio_file = Column(Integer, ForeignKey("audio_file.id"))
    
    f1_freq = Column(Float)
    f2_freq = Column(Float)
    f3_freq = Column(Float)
    f4_freq = Column(Float)
    f5_freq = Column(Float)
    f6_freq = Column(Float)
    
    f1_band = Column(Float)
    f2_band = Column(Float)
    f3_band = Column(Float)
    f4_band = Column(Float)
    f5_band = Column(Float)
    f6_band = Column(Float)
    
class FormantSL(Base):
    __tablename__ = "analysis_formant_sl"
    
    id = Column(Integer,primary_key=True)
    
    audio_file = Column(Integer, ForeignKey("audio_file.id"))
    
    freq = Column(Float)
    
def create_tables(engine):
    Base.metadata.create_all(engine)