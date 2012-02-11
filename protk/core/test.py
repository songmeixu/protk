import os
os.environ["PROTK_DEBUG"] = "YES"

import db
import db.types
from db.types import *

dbconf = {'driver':'sqlite3','name':'/Users/jacobokamoto/Desktop/sqlite.db'}

try:
    
    q = db.get_session(dbconf)
    
    for af in q.query(AudioFile):
        print str(af.filename)
    
    print("db.get_session(%s) --> %s" % (str(dbconf),str(q)))
    a = AudioFile("/Users/jacobokamoto/Developer/work/c3n/SALSA/backend/SALSA-UIMA/data/a-b-c-d-e-f.wav")
    
    q.add(a)
    q.commit()
    
except db.DBConfError:
    print("db.get_engine(%s) --> DBConfError" % dbconf)
except db.DBDriverError:
    print("db.get_engine(%s) --> DBDriverError" % dbconf)
except:
    print("OOPS")
    