'''
Created on Feb 16, 2012

@author: jacobokamoto
'''
from protk.db import Base
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey

    
class FormantBurgParser(object):
    
    def __init__(self, *args, **kwargs):
        self.file = file
        self.formants = []
    
    def parse(self):
        f = open(self.file)
        
        header = []
        for i in range(0,9):
            header.append(f.readline())
        
        x = 0.0
        xstep = 0.00625
        while True:
            intensity = None
            numFormants = None
            formants = []
            try:
                intensity = float(f.readline())
                numFormants = float(f.readline())
            except:
                print "<<EOF>>"
                break
            for i in range(0,int(numFormants*2),2):
                freq = float(f.readline())
                band = float(f.readline())
                formants.append((freq,band))
            
            self.formants.append((x,x+xstep,intensity,formants))
            x+=xstep
            
        return self.formants

class FormantSLParser(object):
    
    def __init__(self, *args, **kwargs):
        self.file = file
        self.formants = []
        
    def parse(self):
        f = open(self.file)
        
        header = []
        for i in range(0,9):
            header.append(f.readline())
            
        x = 0
        xstep = 0.00625
        while True:
            try:
                freq = float(f.readline())
                band = float(f.readline())
                self.formants.append((freq,band))
            except:
                break