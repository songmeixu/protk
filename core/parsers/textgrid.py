import re

class TextGridParser(object):
    
    def __init__(self,filename):
        self.filename = filename

    def parse(self):
        f = open(self.filename)
        line = None
        while True:
            try:
                line = f.readline()
            except:
                break
            if not line:
                break
            isstart = re.search('xmin',line)
            if isstart != None:
                start = float(line.split('=')[1])
            isend = re.search('xmax',line)
            if isend != None:
                end = float(line.split('=')[1])
            isitem = re.search(r'item ?\[\]:',line)
            if isitem != None:
                break

        while True:
            try:
                line = f.readline()
            except:
                break
            if not line:
                break


        print start,end

z = TextGridParser('/home/jacobokamoto/textgrid.txtgrid')
z.parse()
