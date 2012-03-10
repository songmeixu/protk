'''
Created on Mar 7, 2012

@author: jacobokamoto
'''

class ShimmerLocalParser(object):
    def __init__(self, f):
        self.file = f
        self.shimmers = []
    
    def parse(self):
        f = open(self.file)
        ls = f.readlines()
        
        # Get xmin/xmax, number of entries, and step size
        xmin = float(ls[0].split(":")[1])
        xmax = float(ls[1].split(":")[1])
        num_entries = int(float(ls[2].split(":")[1]))
        step = (xmax - xmin) / num_entries
        
        print("[parser][shimmer]> Parsing %d shimmer entries from '%s'" % (num_entries, self.file))
        
        # chop header info
        ls2 = ls[6:]
        # step through data 2 lines at a time
        for val in ls2:
            # append step start/end and pitch to list
            a = val.split(',')
            aval = a[2]
            try:
                aval = float(aval)
            except:
                continue
            self.shimmers.append((float(a[0]),aval))
        return self.shimmers
