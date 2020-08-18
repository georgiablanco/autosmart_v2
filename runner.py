## Author: Kud01
## Date: 12/07/2018

import subprocess

class Runner(object):
    command_line=None
    proc=None
    logger=None
    
#init assigns the premade command line argument to self.
    def __init__(self, logger):
        #self.command_line = command
        self.proc = None
        self.logger = logger

#if blocking is TRUE then the the command is passed as a descriptor/file object to stdout, if FALSE then the command is passed as a descriptor/file object to stdout and you can use communcate???
    def start_run(self, command, blocking):
        self.command_line = command
        self.logger.info("Starting process: %s",self.command_line)
        if (blocking == True):
            self.proc = subprocess.call(self.command_line, shell=False, stdout=subprocess.PIPE)
        else:
            self.proc = subprocess.Popen(self.command_line, shell=False, stdout=subprocess.PIPE)
            # output = self.proc.communicate()[0]
            # print output

    def stop_run(self):
        self.logger.info("Killing process: %s", self.command_line)
        self.proc.kill()
        self.proc = None

# s = subprocess.check_output('tasklist', shell=True)
# if "cmd.exe" in s:
#     print s