from Function import run_process
from Function import getListFile

class Language:
    def __init__(self,name):
        self.name = name        
        
    def compile(self):
        pass
    
    def run(self,timelimit=1,memlimit=1024,stdin=None,stdout=None):
        return run_process(self.name,timelimit,memlimit,stdin,stdout)[2]
        
        
class CPP(Language):
    ext = '.cpp'
    def compile(self):
        stdout, stderr, exitCode = run_process('g++ -std=c++0x -O2 %s.cpp -o %s.exe' % 
            (self.name,self.name),shell=True)
        
        return stderr, exitCode
        
class PAS(Language):
    ext = '.pas'
    def compile(self):
        stdout, stderr, exitCode = run_process('"C:/Program Files/Themis/FPC/bin/i386-win32/fpc.exe" %s.pas -o"%s.exe"' % 
            (self.name, self.name), shell=True)
        return stdout, exitCode
                
        
class JAVA(Language):
    ext = '.java'
    def compile(self):
        stdout, stderr, exitCode = run_process('javac %s.java' % self.name)
        return stderr, exitCode
    
    def run(self,timelimit=1,memlimit=1024,stdin=None,stdout=None):
        if 'Main.class' in getListFile('.'):
            return run_process('java Main', timelimit, memlimit, stdin, stdout)[2]
        return run_process('java %s' % self.name,timelimit,memlimit,stdin,stdout)[2]
        
        
List = {}
List['cpp'] = CPP
List['pas'] = PAS
List['java'] = JAVA
        
if __name__ == "__main__":        
    prob = CPP('other')
    print prob.compile()