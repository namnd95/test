from Function import run_process
#CaculateScore( dict[string,int]result
#dict[string,list]testcase, list[ (score,list) ]subtask )

#return score and verdict
def getScore(score):
    verdict = None
    if score<0:
        if score==-9: verdict = 'TLE'
        else: verdict = 'RE'
        score = 0
    else:
        if score==0: verdict = 'WA'
        elif score<1: verdict = 'PT'
        else: verdict = 'AC'
    return score,verdict
    
CALCULATE_SCORE = {}
def sum(result, testCases, subtask):
    sum = 0
    verdict = ''
    for test, score in result.iteritems():
        verdict+='Test %s: ' % test
        score, state = getScore(score)
        sum += score*testCases[test][-1]
        verdict += state + '\n'        
    return sum,verdict
CALCULATE_SCORE['sum'] = sum

def groupMin(result, testCases, subtask):
    sum = 0
    verdict = ''
    for i in range(len(subtask)):
        AC = 0
        PT = 0
        RE = 0
        TLE = 0
        WA = 0
        value = 1
        for case in subtask[i][1]:            
            score, state = getScore(result[case])            
            value = min(value, score)
            if (state == 'AC'): AC+=1
            elif (state == 'PT'): PT+=1
            elif (state == 'TLE'): TLE+=1
            elif (state == 'RE'): RE+=1
            else: WA+=1
        value *= subtask[i][0]
        sum += value
        verdict += 'Subtask %d: %f\n' % (i+1, value)
        verdict += 'AC: %d,  PT: %d,  WA: %d,  RE: %d,  TLE: %d\n' % (AC,PT,WA,RE,TLE)
            
    return sum,verdict
CALCULATE_SCORE['groupmin'] =  groupMin
STOPPABLE = []
    
#Compare( Input, Output, Answer )
COMPARE = {}
def equal(Input, Output, Answer, Directory):
    try:
        output = open(Output,'r')
        answer = open(Answer,'r')
        
        out=output.read().split(); output.close()
        ans=answer.read().split(); answer.close()
    
        return int(out==ans)
    except:
        return False
COMPARE['equal'] = equal

def externalJudge(Input, Output, Answer, Directory):    
        command = Directory+'check.exe %s %s %s' % (Input, Output, Answer)        
        stdout = run_process(command, shell=True)[0]        
        return int(stdout)        
    #except:
    #    return 0
COMPARE['externalJudge'] = externalJudge

def localCompare(Input, Output, Answer, Directory):
    result = equal(Input, Output, Answer, Directory)
    print result
    return result
COMPARE['localCompare'] = localCompare

def localExternalJudge(Input, Output, Answer, Directory):
    result = externalJudge(Input, Output, Answer, Directory)
    print result
    return result
COMPARE['localExternalJudge'] = localExternalJudge
    
        


if __name__ == "__main__":
    print equal('','file.inp','file.out','')
    
    
