def sep():
    print "------------------------------------------------------------"

print "ProTK Testing Script"
sep()

from core.fs.directory import *

sep()
print "Directory Functions:"
make_empty_dir("/home/jacobokamoto/testdir")
print "list_files: ",list_files("/home/jacobokamoto")
print "list_files: ",list_files("/home/jacobokamoto",include="P")
print "list_files: ",list_files("/home/jacobokamoto",include=["P","D"])
print "list_files: ",list_files("/home/jacobokamoto",exclude=["P","D"])
print "normalize_dir_path: ",normalize_dir_path("/home/jacobokamoto")
print "list_file_paths: ",list_file_paths("/home/jacobokamoto")
sep()

