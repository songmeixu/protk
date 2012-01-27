'''
Created on Jan 26, 2012

@author: jacobokamoto
'''

import os
import os.path

class DirectoryError(IOError):
    
    pass

def bulk_open_from_dir(directory,lines=True):
    """
    Bulk-open files in a given directory
    """
    
    dirparts = directory.split("/")
    dirparts2 = []
    for part in dirparts:
        if part != "":
            dirparts2.append(part)
    
    directory = '/'.join(dirparts2)
    
    if not os.path.exists(directory):
        raise DirectoryError("Directory does not exist '%s'" % (directory))
    
    contents = None
    
    try:
        contents = os.listdir(directory)
    except:
        raise DirectoryError("Could not list directory '%s'" % (directory))
    
    files = {}
    
    for file in contents:
        try:
            contents = os.listdir(directory+"/"+file)
        except:
            f = open(directory+"/"+file)
            if lines:
                files[file] = f.readlines()
            else:
                files[file] = f.read()
            f.close()
    
    return files

def ls(directory):
    if not os.path.exists(directory):
        raise DirectoryError("Directory does not exist '%s'" % (directory))
    
    contents = None
    
    try:
        contents = os.listdir(directory)
    except:
        raise DirectoryError("Could not list directory '%s'" % (directory))
    return contents

print ls("C:/Users")