import os,sys

class PathDoesNotExist(Exception):
    pass
class FileDoesNotExist(Exception):
    pass
class DirDoesNotExist(Exception):
    pass
class DirListError(Exception):
    pass

def get_filenames(directory,filter_by=None):
    try:
        ls = os.listdir(directory)
        new = []
        for entry in ls:
            if entry.startswith('.'):
                continue
            if filter_by != None:
                if entry.find(filter_by) == -1:
                    continue
                else:
                    new.append(entry)
            else:
                new.append(entry)
        return new
    except:
        raise DirListError()