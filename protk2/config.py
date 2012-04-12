'''
Created on Mar 17, 2012

@author: jacobokamoto
'''
DATABASE = {'driver':'sqlite3','name':'sqlite.db'}

ARFF_FEATURES = {
                 'pitch':('mean','median','stdev','slope','minval','maxval'),
                 'shimmer':('mean','median','stdev','slope','minval','maxval'),
                 'jitter':('mean','median','stdev','slope','minval','maxval'),
                 'intensity':('mean','median','stdev','slope','minval','maxval'),
                 'f1':('mean','median','stdev','slope','minval','maxval'),
                 'f2':('mean','median','stdev','slope','minval','maxval'),
                 }

ARFF_SHOW_WORD = False
ARFF_CONTEXT_SIZE = 0

ARFF_CLASSIFY_COMMAND = """java -cp weka.jar weka.classifiers.functions.SMO -l %s -T %s -p 0 > %s"""