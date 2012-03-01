'''
protk.parsers.prosody.textgrid
 |
 +- TextGridParser

@author: jacobokamoto
'''

import re,os,sys

from protk.db import DatabaseManager
from protk.db.types.prosody import Word,Phone
from protk.db.types import AudioFile

FOUND_ITEM = -1
FOUND_INTERVAL = -2
FOUND_EOF = -3
MAXEMPTY = 10

class TextGridParser(object):
    
    def __init__(self,filename, prosody_collection):
        self.filename = filename
        self.prosody_collection = prosody_collection
        self.contents = []
        
    def parse(self):
        fh = open(self.filename)
        f = fh.readlines()
        # parse the header
        self._parse_header(f)
        # start parsing items
        self._parse_items(f)
        return self.contents
        
    def _parse_header(self,f):
        line = None
        while True:
            if len(f) > 0: line = f[0]
            
            if line == None: break
            if len(line.strip()) == 0:
                f.pop(0)
                continue
            
            if re.search("ooTextFile",line):
                #print("[parser][txtgrid]> Reading 'ooTextFile'")
                pass
                
            elif re.search("TextGrid",line):
                #print("[parser][txtgrid]> + File is a textgrid. Good.")
                pass
                
            elif re.search("xmin",line):
                self.start = float(line.split('=')[1])
                #print("[parser][txtgrid]> + Start time: %f" % self.start)
                
            elif re.search("xmax",line):
                self.end = float(line.split('=')[1])
                #print("[parser][txtgrid]> + End time: %f" % self.end)
                
            elif re.search("tiers?",line) and re.search("exists",line):
                #print("[parser][txtgrid]> + Has tiers...")
                pass
                
            elif re.search("size",line):
                self.size = int(line.split('=')[1])
                #print("[parser][txtgrid]> + Tier count: %d"%self.size)
                
            elif re.search("item",line) and re.search(r"\[\]",line):
                #print("[parser][txtgrid]> Reached start of items")
                return line
            
            else:
                #print("[parser][txtgrid]> Unkonwn parameter in line '%s'" % line)
                pass
                
            if len(f) > 0: f.pop(0)
                
    def _parse_items(self,f):
        line = None
        found_item = False
        while True:
            if not found_item and len(f) > 0: line = f[0]
            elif len(f) == 0: return False
            
            if line == None: return False
            if len(line.strip()) == 0:
                f.pop(0)
                continue
            
            if re.search("item[ ]*\[\d+\]",line) or found_item:
                #print("[parser][txtgrid]> Found an item...")
                found_item = self._parse_item(f)
                #print("[parser][txtgrid]> Item parsed.")
            else:
                f.pop(0)
                continue
                
            if len(f) > 0: f.pop(0)
                
    def _parse_item(self,f):
        line = None
        found_interval = False
        while True:
            if not found_interval:
                if len(f) > 0:
                    line = f[0]
                else: return False
            
            if len(f) == 0: return False
            if line == None: return False
            if len(line.strip()) == 0:
                f.pop(0)
                continue
            
            if re.search("item[ ]*\[\d+\]",line): return True
            elif re.search("class",line) and re.search("[Ii]nterval[Tt]ier",line):
                #print("[parser][txtgrid][item]> Reading item")
                pass
            elif re.search("name[ ]*=",line):
                item_type = line.split("=")[1].strip().strip('"')
                #print("[parser][txtgrid][item]> + Item type: %s" % item_type)
            elif re.search("xmin",line):
                start = float(line.split('=')[1])
                #print("[parser][txtgrid][item]> + Start time: %f" % self.start)
            elif re.search("xmax",line):
                end = float(line.split('=')[1])
                #print("[parser][txtgrid][item]> + End time: %f" % self.end)
            elif re.search("intervals[ ]*\[\d+][ ]*:",line):
                #print("[parser][txtgrid][item]["+item_type+"]> Found a new "+item_type)
                #if len(f) > 0: f.pop(0) # apparently this line broke stuff. Oops.
                found = self._parse_interval(f,item_type)
                #print("[parser][txtgrid][item]> Parsed item.")
                if found == FOUND_ITEM: return True
                elif found == FOUND_INTERVAL: found_interval = True
                elif found == FOUND_EOF: return False
            else:
                #print("[parser][txtgrid][item]> Unknown line...")
                pass
                
            if len(f) > 0: f.pop(0)
                
    def _parse_interval(self,f,label="interval"):
        line = None
        start = None
        end = None
        text = None
        extdata = {}
        found = -100
        while True:
            if len(f) > 0:
                line = f[0]
            else:
                found = FOUND_EOF
                break
            
            if line.strip() == "": found = FOUND_EOF
            if len(line.strip()) == 0:
                f.pop(0)
                continue
            
            if re.search("item[ ]*\[\d+\]",line): 
                found = FOUND_ITEM
                break
            elif re.search("intervals[ ]*\[\d+][ ]*:",line):
                found = FOUND_INTERVAL
                break
            elif re.search("text[ ]*=",line):
                text = line.split("=")[1].strip().strip('"')
                #print("[parser][txtgrid][item]["+label+"]> + Text: %s" % item_type)
            elif re.search("xmin",line):
                start = float(line.split('=')[1])
                #print("[parser][txtgrid][item]["+label+"]> + Start time: %f" % start)
            elif re.search("xmax",line):
                end = float(line.split('=')[1])
                #print("[parser][txtgrid][item]["+label+"]> + End time: %f" % end)
            elif len(line.split('=')) == 2:
                spl = [i.strip() for i in line.split('=')]
                #print("[parser][txtgrid][item]["+label+"]> + Extra: '%s' = '%s'"%(str(spl[0]),str(spl[1])))
            if len(f) > 0: f.pop(0)
            
        if label.lower() == "word" and start != None and end != None and text != None:
            print self.prosody_collection.id
            w = Word(self.prosody_collection, start, end, text, extdata)
            self.contents.append(w)
        elif label.lower() == "phone" and start != None and end != None and text != None:
            p = Phone(self.prosody_collection, start, end, text, extdata)
            self.contents.append(p)
        
        return found


"""
from protk.db.types import create_tables as create_base_tables
from protk.db.types.analysis import create_tables as create_analysis_tables
from protk.db.types.prosody import create_tables as create_prosody_tables
                       
a = AudioFile()
d = DatabaseManager({'driver':'sqlite3','name':'/home/jacobokamoto/testdata/sqlite.db'})
s = d.get_session()

create_base_tables(d.engine)
create_prosody_tables(d.engine)

z = TextGridParser("/home/jacobokamoto/testdata/test.txtgrid",a)
z.parse()
print [str(i) for i in z.contents]
print len(z.contents)
s.add_all(z.contents)
s.commit()
print "Done..."
"""