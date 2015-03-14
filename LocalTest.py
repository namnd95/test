from Problem import Problem
from Submission import Submission
import Language

if __name__ == "__main__": 
    #problem = Problem('exchange', 'D:/Problem/ad-hoc/exchange/', Comp='localCompare')    
    problem = Problem('sort', 'D:/Problem/ad-hoc/sort/', Comp='localCompare')
    language = Language.List['pas'](problem.id)
    location = 'D:/BT/TMP/New folder/sort.pas'
    #location = 'D:/Problem/DP/block/block.cpp'
    #for key,value in problem.testCases.iteritems(): print key,value
    now = Submission(problem, language, location)            
    result, verdict = now.process()    
    print result
    print verdict