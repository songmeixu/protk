'''
Created on Feb 3, 2012

@author: jacobokamoto
'''
# Import SQLAlchemy types for ORM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy import ForeignKey

Base = declarative_base()

class ProsodyCollection(Base):
    """
    Prosodic data collections (this would be the top level of a
    Praat TextGrid file)
    """
    
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True)
    collection_name = Column(String(255))
    

class ProsodyTier(Base):
    """
    Prosodic data tier (e.g., phone or word tier)
    """
    __tablename__ = "collection_tiers"
    
    id = Column(Integer, primary_key=True)
    
    collection_id = Column(Integer,ForeignKey("collections.id"))
    
    tier_name = Column(String(255))

class ProsodyData(Base):
    """
    Data element of a prosody tier
    """
    
    __tablename__ = "collection_tier_data"
    
    id = Column(Integer, primary_key=True)
    
    tier_id = Column(Integer,ForeignKey("collection_tiers.id"))
    
    xmin = Column(Float)
    xmax = Column(Float)
    
    data = Column(Text)