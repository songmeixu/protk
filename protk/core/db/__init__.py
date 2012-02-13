from sqlalchemy import create_engine
import types

class DBConfError(Exception):
    pass
class DBDriverError(Exception):
    pass
class DBEngineError(Exception):
    pass

"""
DATABASE ENGINE
"""
def get_engine(dbconf):
    
    # Verify that an actual database configuration was passed in
    if not dbconf:
        raise DBConfError("Please provide a database configuration")
    
    # Check for a driver key
    if dbconf.has_key('driver'):
        if dbconf['driver'] == 'sqlite3' and dbconf.has_key('name'):
            # Try to create the engine and raise an error if it can't be created
            try:
                z = create_engine('sqlite:///%s' % dbconf['name'])
                return z
            except Exception:
                raise DBEngineError("Could not create the database engine. Check configuration")
    # Raise an error if no driver is specified
    else:
        raise DBDriverError("A database driver was not specified.")

def create_db(engine):
    types.Base.metadata.create_all(engine)

"""
DATABASE SESSION
"""
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
session_configured = False

def get_session(dbconf):
    global Session
    global session_configured
    if not session_configured:
        engine = get_engine(dbconf)
        create_db(engine)
        Session.configure(bind=engine)
        session_configured=True
    return Session()

from types import *
              
class DatabaseManager(object):
    
    def __init__(self, configuration):
        self.configuration = configuration
        self.engine = get_engine(configuration)
        self.sessionmaker = sessionmaker()
        create_db(self.engine)
        self.sessionmaker.configure(bind=self.engine)
        self.session = None
        
    def get_session(self):
        if self.session == None:
            self.session = self.sessionmaker()
        return self.session
    
    def dump_data(self):
        print "Dumping all data from database"
        files = self.session.query(AudioFile)
        for file in files:
            print "[file]> %s" % file.filename
            collections = self.session.query(ProsodyCollection).filter_by(audio_file=file.id)
            for collection in collections:
                print "[prosody]> Collection:", "truth" if collection.collection_type == ProsodyCollection.Types.Truth else "training"
                tiers = self.session.query(ProsodyTier).filter_by(collection=collection.id)
                for tier in tiers:
                    print "[prosody]>> Tier:", tier.tier_type
                    ivals = self.session.query(ProsodyData).filter_by(tier=tier.id)
                    for ival in ivals:
                        print "[prosody]>>> Interval: %f to %f sec; content: %s" % (ival.xmin,ival.xmax,ival.value)
