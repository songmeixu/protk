'''
Created on Mar 7, 2012

@author: jacobokamoto
'''

class IntensityParser(object):
    def __init__(self, f):
        self.file = f
        self.intensities = []
    
    def parse(self):
        f = open(self.file)
        ls = f.readlines()
        
        # Get xmin/xmax, number of entries, and step size
        xmin = float(ls[3])
        xmax = float(ls[4])
        num_entries = int(ls[5])
        step = (xmax - xmin) / num_entries
        
        print("[parser][pitch]> Parsing %d intensity entries from '%s'" % (num_entries, self.file))
        
        # chop header info
        ls2 = ls[13:]
        # step through data 2 lines at a time
        for val in ls2:
            # append step start/end and pitch to list
            self.intensities.append(float(val))
        return self.intensities
