'''
Created on Feb 29, 2012

@author: jacobokamoto
'''

class SilenceParser(object):
    def __init__(self, f):
        self.file = f
        self.silences = []
        self.soundings = []
        
    def parse(self):
        f = open(self.file)
        ls = f.readlines()
        
        num_parts = int(ls[11])
        ls2 = ls[12:]
        for i in range(0,len(ls2),3):
            s = float(ls2[i])
            e = float(ls2[i+1])
            t = ls2[i+2]
            if t == "silent": self.silences.append((s,e))
            else: self.soundings.append((s,e))
            
        return {'silences': self.silences, 'soundings': self.soundings}