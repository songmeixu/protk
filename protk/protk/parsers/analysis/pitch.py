'''
Created on Feb 29, 2012

@author: jacobokamoto
'''

class PitchParser(object):
    def __init__(self, f):
        self.file = f
        self.pitches = []
    
    def parse(self):
        f = open(self.file)
        ls = f.readlines()
        
        # Get xmin/xmax, number of entries, and step size
        xmin = float(ls[3])
        xmax = float(ls[4])
        num_entries = int(ls[5])
        step = (xmax - xmin) / num_entries
        
        print("[parser][pitch]> Parsing %d pitch entries from '%s'" % (num_entries, self.file))
        
        # chop header info
        ls2 = ls[6:]
        # step through data 2 lines at a time
        for i in range(0,len(ls2),2):
            # get actual step
            istep = i/2
            # append step start/end and pitch to list
            self.pitches.append((step*istep,step*(istep+1),float(ls2[i+1])))
            
        return self.pitches

