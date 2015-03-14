from Problem import Problem
from Function import getListFile, getListDir
import Judge
import Language
import os
from shutil import copy2


def cleanUp(Keep=[], flag=True):
    for file in getListFile('.'):
        if not file in Keep: os.remove(file)
    if flag: os.chdir('..')

class Submission:
    def __init__(self, problem, language, location):
        #os.chdir('RunningRoom')
        #cleanUp()
        self.problem = problem
        self.language = language
        copy2(location, './RunningRoom/'+language.name+language.ext)
        print location
        print './RunningRoom/'+language.name+language.ext
        
    
    #return score and verdict
    
    def process(self):        
        os.chdir('RunningRoom')
        oldFile = getListFile('.')
        stderr, exitCode = self.language.compile()        
        #print oldFile
        if exitCode != 0:
            cleanUp()
            return 0, 'Compile Error\n'+stderr
        
        newFile = []        
        for file in getListFile('.'):
            if not file in oldFile: newFile.append(file)
        #print newFile
        
        score = {}        
        for id_case, case in self.problem.testCases.iteritems():
            cleanUp(newFile,False)
            dir = self.problem.directory
            
            #copy file input if have file input
            try:
                copy2(dir+case[0],self.problem.default_case[0])
            except:
                pass
            
            exitCode = self.language.run(case[2],case[3],
                self.problem.stdin,self.problem.stdout)
            if exitCode != 0:
                if (exitCode == 1): exitCode = -9 #Windows exit code to Unix
                if exitCode > 0: exitCode = -exitCode
                score[id_case] = exitCode
            else:
                result = self.problem.compare(dir+case[0], 
                    self.problem.default_case[1], dir+case[1],
                    self.problem.directory)
                score[id_case] = result
            if score[id_case]<=0 and self.problem.canStop: break
            print 'finish %s' % id_case
        
        cleanUp()        
        return self.problem.calculateScore(score,
            self.problem.testCases,self.problem.subtask)

def LoadProblem():
    FileProblem = open('problem.txt','r')
    ProblemList = {}
    for line in FileProblem:        
        problem = line.split()
        ProblemList[problem[0]] = Problem(problem[0],problem[1])
    FileProblem.close()
    return ProblemList
        
if __name__ == "__main__":    
    ProblemList = LoadProblem()    
    #print ProblemList
    while True:
        #prob, language, location = [x for x in raw_input().split()]
        prob, language, location = ['game', 'cpp', 'D:/Problem/greedy/game/game.cpp']
        now = Submission(ProblemList[prob],
            Language.List[language](prob), location)
        result, verdict = now.process()
        print result
        print verdict
        break
    