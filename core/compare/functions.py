import config
from result import Result

def compareLineIgnoreSpace(line, out, ans, compareFunction):
    out = out.split()
    ans = ans.split()
    if len(out) != len(ans):
        return Result(score=0, verdict='Line %d length mismatch' % line)
    
    for i in xrange(len(out)):
        if compareFunction(out[i], ans[i])==0:
            return Result(
                score=0,
                verdict='Line %d at %d output %s answer %s' % 
                    (line, i+1,out[i],ans[i])
            )
    
    return None

def compareIgnoreSpace(output, answer, compareFunction):
    try:
        fileOut = open(output,'r')
        fileAns = open(answer,'r')
        
        out = fileOut.read().split('\n')
        ans = fileAns.read().split('\n')
        
        fileOut.close()
        fileAns.close()
    except:
        return Result(score=0, verdict='No output found')
    
    if len(out) != len(ans):
        return Result(score=0, verdict='Lines mismatch')
    
    for i in xrange( len(out) ):
        value = compareLineIgnoreSpace(i+1, out[i], ans[i], compareFunction)
        if value is not None:
            return value
    
    return Result(1, 'AC')
    
def equal(output, answer):
    return int(output==answer)
    
def equalWithEpsilon(output, answer):
    try:
        out = float(output)
        ans = float(answer)
    except:
        return 0
    
    return int(abs(out-ans) < 1e-6)
    
def equalIgnoreSpace(output, answer, *args, **kargs):
    return compareIgnoreSpace(output, answer, equal)
config.update(equalIgnoreSpace)    
    
def equalIgnoreSpaceEpsilon(output, answer, *args, **kargs):
    return compareIgnoreSpace(output, answer, equalWithEpsilon)
config.update(equalIgnoreSpaceEpsilon)
