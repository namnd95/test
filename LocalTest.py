from Problem import Problem
from Submission import Submission
import Language

if __name__ == "__main__":
    # problem = Problem('exchange', 'D:/Problem/graph/petrol/', Comp='localCompare')
    problem = Problem(
        'file',
        'D:/AMM2/Contests/SPOJ/exams/doncay/',
        Comp='localExternalJudge')
    # problem = Problem('file', 'D:/Projects/VM15/round4/vmcut2/tests/', Comp='localCompare')
    language = Language.List['pas'](problem.id)
    # location = 'D:/Projects/VM15/round4/vmcut2/sol_bao.cpp'
    # location = 'D:/Problem/graph/petrol/sol.cpp'
    location = 'D:/BT/SPOJ/vodoncay.pas'
    # for key,value in problem.testCases.iteritems(): print key,value
    now = Submission(problem, language, location)
    result, verdict = now.process()
    print result
    print verdict
