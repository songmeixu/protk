from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, UniqueConstraint, ForeignKey
import pickle

Base = declarative_base()

class AudioFile(Base):
    __tablename__ = "audio_file"

    id = Column(Integer,primary_key=True)

    filename = Column(String(255))
    hashname = Column(String(255))

    extdata = Column(Text)

    def set_extdata(self,data):
        self.extdata = pickle.dumps(data)
    def get_extdata(self):
        if extdata != None and extdata != "":
            return pickle.loads(self.extdata)
        else:
            return None

class ProsodyCollection(Base):
    __tablename__ = "prosody_collection"

    id = Column(Integer,primary_key=True)
    audio_file = Column(Integer,ForeignKey("audio_file.id"))
    collection_type = Column(Integer)
    extdata = Column(Text)

class Word(Base):
    __tablename__ = "prosody_word"

    id = Column(Integer,primary_key=True)

    collection = Column(Integer,ForeignKey("prosody_collection.id"))

    start_time = Column(Float)
    end_time = Column(Float)

    duration = Column(Float)

    word = Column(String(255))

    extdata = Column(Text)

class Phone(Base):
    __tablename__ = "prosody_phone"

    id = Column(Integer,primary_key=True)

    collection = Column(Integer,ForeignKey("prosody_collection.id"))

    start_time = Column(Float)
    end_time = Column(Float)

    duration = Column(Float)

    phone = Column(String(255))

    extdata = Column(Text)

class Label(Base):
    __tablename__ = "prosody_label"
    
    id = Column(Integer,primary_key=True)

    collection = Column(Integer,ForeignKey("prosody_collection.id"))

    label_type = Column(String(64))

    start_time = Column(Float)
    end_time = Column(Float)

    duration = Column(Float)

    data = Column(String(255))

    extdata = Column(Text)


