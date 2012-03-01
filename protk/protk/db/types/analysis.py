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
    
    xmin = Column(Float)
    xmax = Column(Float)
    
    intensity = Column(Float)
    
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
    
    def __init__(self,audio_file, xmin,xmax,intensity,formants):
        i = 1
        for formant in formants:
            if i == 1:
                self.f1_freq = formant[0]
                self.f1_band = formant[1]
            elif i == 2:
                self.f2_freq = formant[0]
                self.f2_band = formant[1]
            elif i == 3:
                self.f3_freq = formant[0]
                self.f3_band = formant[1]
            elif i == 4:
                self.f4_freq = formant[0]
                self.f4_band = formant[1]
            elif i == 5:
                self.f5_freq = formant[0]
                self.f5_band = formant[1]
            elif i == 6:
                self.f6_freq = formant[0]
                self.f6_band = formant[1]
            else: continue
            
            i+=1
        self.xmin = xmin
        self.xmax = xmax
        self.intensity = intensity
        self.audio_file = audio_file.id
        
class FormantSL(Base):
    __tablename__ = "analysis_formant_sl"
    
    id = Column(Integer,primary_key=True)
    
    audio_file = Column(Integer, ForeignKey("audio_file.id"))
    
    xmin = Column(Float)
    xmax = Column(Float)
    freq = Column(Float)
    
    def __init__(self, audio_file, xmin, xmax, freq):
        self.audio_file = audio_file.id
        self.xmin = xmin
        self.xmax = xmax
        self.freq = freq

def create_tables(engine):
    Base.metadata.create_all(engine)