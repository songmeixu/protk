import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConfigurationError(Exception):
    pass
class DBDriverError(Exception):
    pass
class DBEngineError(Exception):
    pass

class DatabaseManager(object):

    def __init__(self, dbconf):
        self.dbconf = dbconf
        self.sessionmaker = sessionmaker()
        self.session = None
        self.engine = None

        get_engine()


    def get_engine(self):
        # Verify that an actual database configuration was passed in
        dbconf = self.dbconf
        
        if self.engine != None:
            return self.engine

        if not dbconf:
            raise DBConfError("Please provide a database configuration")
            
        # Check for a driver key
        if dbconf.has_key('driver'):
            if dbconf['driver'] == 'sqlite3' and dbconf.has_key('name'):
                # Try to create the engine and raise an error if it can't be created
                try:
                    self.engine = create_engine('sqlite:///%s' % dbconf['name'])
                except Exception:
                    self.engine = None
                    raise DBEngineError("Could not create the database engine. Check configuration")
        # Raise an error if no driver is specified
        else:
            raise DBDriverError("A database driver was not specified.")

    def create_db(engine, decl_base):
        decl_base.metadata.create_all(engine)

    def get_session(dbconf):
        if self.session == None:
            if self.engine == None:
                self.get_engine()
            self.sessionmaker.configure(bind=engine)
            self.session = self.sessionmaker()

        return self.session

