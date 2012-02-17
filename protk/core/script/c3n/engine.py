'''
Created on Feb 12, 2012

Praat script generation module

@author: jacobokamoto
'''

from core.fs import get_filenames
from config import C3N_PRAAT_SCRIPT,C3N_PRAAT_DEFAULT_OPTIONS,C3N_PRAAT_PRAAT_OPTIONS
import config

import os,sys,shutil,time,subprocess,multiprocessing
class C3NPraatProcessor:
    def generate_script(self, input_file):
        script_file = open(self.script_dir+input_file+".praat",'w')
        print "[praat][script][generate]> Generating script for '%s' at '%s'" % (input_file,self.script_dir+input_file+".praat")
        script_template = C3N_PRAAT_SCRIPT
        for option,values in self.options.iteritems():
            script_template = script_template.replace(values[2],('1' if values[0] else '0'))
        
        script_template = script_template.replace('<<inputdir>>',self.input_dir).replace('<<inputfile>>',input_file)
        try:
            os.mkdir(self.output_dir+input_file+'/')
        except:
            shutil.rmtree(self.output_dir+input_file+'/')
            os.mkdir(self.output_dir+input_file+'/')
        script_template = script_template.replace('<<outputdir>>',self.output_dir+input_file+'/').replace('<<inputname>>',(input_file.split(".")[0].replace(' ','_')))
        script_file.write(script_template)
        
    def generate_scripts(self):
        for f in self.input_files:
            self.generate_script(f[0])
    
    def run_scripts(self):
        print "[praat][script]> Entering execute mode"
        print "[praat][script][exec]> Starting script execution"
        scripts = get_filenames(self.script_dir)
        scripts = [self.script_dir+i for i in scripts]
        num = len(scripts)
        
        # Iterate through the scripts and spawn as many worker processes
        # as there are CPUs reported by the multiprocessing module
        
        active_processes = set()    # Active processes tracking variable
        max_processes = multiprocessing.cpu_count() # CPU count determines max processes
        binary = self.praatOptions["binary"] # get the binary used with Praat
        
        print "[praat][script][exec]> Using Praat binary at '%s'" % binary
        
        
        for script in scripts:
            active_processes.add(subprocess.Popen([binary,script]))
            print "[praat][script][exec][subproc]> Spawning Praat processor with script '%s'" % script
            if len(active_processes) >= max_processes:
                os.wait()
                print "[praat][script][exec]> Subprocess completed."
                active_processes.difference_update([p for p in active_processes if p.poll() is not None])
                
        while True:
            try:
                os.wait()
                print "[praat][script][exec]> Subprocess completed."
            except:
                print "[praat][script][exec]> All processes completed"
                break
            
        
    def __init__(self, input_dir, script_dir, output_dir, options=None, praatOptions=None):
        # Fix directory paths (all with trailing slash)
        self.input_dir = input_dir+'/' if input_dir[-1]!='/' else input_dir
        self.output_dir = output_dir+'/' if output_dir[-1]!='/' else output_dir
        self.script_dir = script_dir+'/' if script_dir[-1]!='/' else script_dir
        
        # initialize instance vars
        self.options = None
        self.praatOptions = None
        
        # set default Praat options if none provided
        if praatOptions != None: self.praatOptions = praatOptions
        else: self.praatOptions = C3N_PRAAT_PRAAT_OPTIONS
        self.input_files = None
        self.command_opts = ""  # vestigial?
        
        if not options:
            # also vestigial?
            self.options = C3N_PRAAT_DEFAULT_OPTIONS
            for option,value in self.options.iteritems():
                self.command_opts += " "+option+('1' if value else '0')
            print self.command_opts
            
            # load input file list
            try:
                input_files = get_filenames(input_dir, ".wav")
                self.input_files = []
                for f in input_files:
                    self.input_files.append((f,(f.split(".")[0].replace(' ','_'))))
            except:
                raise Exception("[praat][init]> ERROR: Input directory does not exist.")
            
            # make generated script directory
            if not os.path.exists(self.script_dir):
                os.makedirs(self.script_dir, 0775)
                print "[praat][init]> Created script directory '%s'" % self.script_dir
            elif not os.path.isdir(self.script_dir):
                raise OSError("[praat][init]> Script path does not point to a directory '%s'" % self.script_dir)
            else:
                shutil.rmtree(self.script_dir)
                os.makedirs(self.script_dir, 0775)
                print "[praat][init]> Using script directory '%s' (cleaned)" % self.script_dir
            
            # make output data directory
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir, 0775)
                print "[praat][init]> Created output directory '%s'" % self.output_dir
            elif not os.path.isdir(self.output_dir):
                raise OSError("[praat][init]> Output path does not point to a directory '%s'" % self.output_dir)
            else:
                print "[praat][init]> Using output directory '%s'" % self.output_dir
            
    
            
z = C3NPraatProcessor("C:/Users/jacobokamoto/Desktop/testdata/wav/","C:/Users/jacobokamoto/Desktop/testdata/scripts/","C:/Users/jacobokamoto/Desktop/testdata/output/")
z.generate_scripts()
z.run_scripts()