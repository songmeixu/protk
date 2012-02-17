import sqlalchemy
from sqlalchemy import create_engine

class DBConfigurationError(Exception):
    pass
class DBDriverError(Exception):
    pass
class DBEngineError(Exception):
    pass

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

def create_db(engine, decl_base):
    decl_base.metadata.create_all(engine)
