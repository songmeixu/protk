'''
Created on Feb 9, 2012

This is the basic configuration file for ProTK

@author: jacobokamoto
'''

PROTK_DEBUG=True

PROTK_VERSION='0.0.1-DEVELOPMENT-DEMONSTRATOR'

DATABASE =  {
            'driver' : 'sqlite3',       # For most cases, this should be 'sqlite3'
            'name'   : 'sqlite.db',     # The path to the database file
            }

TAGS =      {
              'filled_pause_tags' : {
                                     'um' : 'FPU',
                                     'ah' : 'FPA',
                                     }
            }
