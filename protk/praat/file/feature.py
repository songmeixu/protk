'''
Created on Jan 26, 2012

@author: jacobokamoto
'''

import re

def read_features(filename):
    
    f = None
    
    try:
        f = open(filename)
    except IOError:
        print ">> Could not open feature file at '%s'" % (filename)
        return None
        
    lines = f.readlines()
    
    ret = []
    
    for line in lines:
        val = None
        try:
            val = float(line)
        except ValueError:
            if re.search('--undefined--',line) != None:
                val = float("inf")
            else:
                val = None
        
        if val != None:
            ret.append(val)
            print val
            
    for val in ret:
        print val
        

        
read_features('C:\\Users\\jacobokamoto\\Desktop\\praatOutput\\a-b-c-d-e-f_Short\\a-b-c-d-e-f.JitterLocal')