'''
Created on Jan 23, 2012

@author: jacobokamoto
'''

from textgrid import TextGrid

print "Hello"

t = TextGrid("C:/Users/jacobokamoto/Developer/work/c3n/protk/work/truth/tmp.txtgrid")

t.add_to_db()
"""
for tier in t.tiers:
    print tier.type
    for interval in tier.intervals:
        print interval.xmin,interval.xmax
        """