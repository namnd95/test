import os
import Judge
from Function import getListFile, getListDir


def isFileOut(FileOut):
    return ('.out' in FileOut) or ('.ans' in FileOut) \
        or ('.a' in FileOut) or ('output' in FileOut)


def isFileIn(FileIn):
    return ('.inp' in FileIn) or ('.in' in FileIn) \
        or ('input' in FileIn)


def isNotFileIn(FileIn):
    return ('.cpp' in FileIn) or ('.py' in FileIn) \
        or ('.pas' in FileIn) or ('.c' in FileIn) \
        or ('.exe' in FileIn) or ('file.inp' in FileIn)
"""
CLASS PROBLEM
    STATIC VARIBLES:
        FILE: file that not considered in input or output
        DEFAULT: default value
        VALUE: constant in .config
        DEFAULT_CONFIG: config that use in default without .config
    varibles:
        id              :name of problem
        directory       :the folder of problem
        testCases       :testCase of problem. With each testcase:
                            testid: fileIn, fileOut, timelimit, memlimit, score
        default_case    :fileIn, fileOut of the source
                            timelimit, memlimit, score by default
                            if testcase use default setting value is DEFAULT
        config          :including
                            stdin: True/False: input use stdin or not
                            stdout: True/False: output use stdout or not
                            judge: how to calculateScore
                            compare: how to compare output
        subtask         :each subtask include a list of testid
        canStop         :True if can stop after a fail testcase

CONFIG FILE FORMAT:

"""


class Problem:

    FILE = ['.config', '.testcase', '.subtask', '']
    DEFAULT = '_DEFAULT'
    VALUE = {'True': True, 'False': False,
             'sum': Judge.sum, 'groupmin': Judge.groupMin,
             'equal': Judge.equal}
    DEFAULT_CONFIG = {'stdin': 'False', 'stdout': 'False',  # Need change
                      'Judge': 'sum', 'Comp': 'equal'}

    def refresh(self, createFiles):
        self.loadTestcase(createFiles)
        self.loadConfig(createFiles)
        self.loadSubtask()

    def __init__(self, id='', directory='', createFiles=False, **kargs):
        self.id = id
        self.directory = directory
        # testid, [filein, fileout, timelimit, memlimit, score]
        self.testCases = {}
        self.default_case = [id + '.inp', id + '.out', 2, 1024, 1]
        self.config = {}
        self.subtask = []
        for key, value in kargs.iteritems():
            print key, value
            self.DEFAULT_CONFIG[key] = value

        self.refresh(createFiles)

    # convert to float
    def convert(self, x):
        result = x
        try:
            result = float(x)
        except:
            pass
        return result

    def loadSubtask(self):
        try:
            fileSubtask = open(self.directory + '.subtask', 'r')
            self.subtask = []
            n = -1
            for line in fileSubtask:
                line = line.split()
                if (len(line) == 0):
                    continue
                line = line[0]
                if line[0] == '#':  # begin subtask:
                    n += 1
                    self.subtask.append((int(line[1:]), []))  # remove #
                else:
                    self.subtask[n][1].append(line)
            fileSubtask.close()
        except:
            pass

    # WRITE TO FILE .config
    def writeConfig(self):
        fileConfig = open(self.directory + '.config', 'w')
        for key, value in self.DEFAULT_CONFIG.iteritems():
            fileConfig.write('%s: %s\n' % (key, value))
        fileConfig.close()

    def loadConfig(self, createFiles):
        try:
            fileConfig = open(self.directory + '.config', 'r')
            for line in fileConfig:
                cur = line.split()
                self.config[cur[0][:-1]] = cur[1]  # Delete':' | name: value
            fileConfig.close()
        except:
            for key, value in self.DEFAULT_CONFIG.iteritems():
                self.config[key] = value
            if createFiles:
                self.writeConfig()
        # load each value in config
        if self.config['stdin'] == 'False':
            self.stdin = None
        else:
            self.stdin = self.default_case[0]
        if self.config['stdout'] == 'False':
            self.stdout = None
        else:
            self.stdout = self.default_case[1]
        self.calculateScore = Judge.CALCULATE_SCORE[self.config['Judge']]
        self.compare = Judge.COMPARE[self.config['Comp']]
        self.canStop = self.calculateScore in Judge.STOPPABLE

    # WRITE TO FILE .testcase
    def writeTestcase(self):
        fileTestcase = open(self.directory + '.testcase', 'w')
        for value in self.default_case:
            fileTestcase.write('%s ' % value)
        fileTestcase.write('\n')

        for id_case, case in self.testCases.iteritems():
            fileTestcase.write('%s ' % id_case)
            for i in range(len(case)):
                d = case[i]
                if d == self.default_case[i]:
                    d = self.DEFAULT
                fileTestcase.write('%s ' % d)
            fileTestcase.write('\n')
        fileTestcase.close()

    def loadTestcase(self, createFiles):
        try:
            fileTestcase = open(self.directory + '.testcase', 'r')
            cur = fileTestcase.readline().split()
            for i in xrange(2, len(cur)):
                cur[i] = float(cur[i])
            self.default_case = cur
            for line in fileTestcase:
                cur = line.split()
                id = cur.pop(0)
                for i in range(len(cur)):
                    if cur[i] == self.DEFAULT:
                        cur[i] = self.default_case[i]
                for i in xrange(2, len(cur)):
                    cur[i] = float(cur[i])
                self.testCases[id] = cur
            fileTestcase.close()
        except:
            subDir = getListDir(self.directory)
            if len(subDir) == 0:
                # testcase not in subfolder
                listFile = getListFile(self.directory)
                fileIn = []
                fileOut = []
                for file in listFile:
                    if isFileOut(file):
                        fileOut.append(file)
                    elif not isNotFileIn(file):
                        fileIn.append(file)
                fileIn.sort()
                fileOut.sort()
                for i in range(len(fileOut)):
                    # Get test id is the name before extension
                    id = fileOut[i][:fileOut[i].rfind('.')]
                    self.testCases[id] = [fileIn[i], fileOut[i]]
                    for i in xrange(2, len(self.default_case)):
                        self.testCases[id].append(self.default_case[i])
            else:
                # test cases like Themis testCases
                for dir in subDir:  # name of testCases
                    ListFile = getListFile(self.directory + dir)
                    fileIn = ListFile[0]
                    fileOut = ListFile[1]
                    if isFileOut(fileIn):
                        fileIn, fileOut = fileOut, fileIn
                    self.testCases[dir] = [
                        dir + '/' + fileIn, dir + '/' + fileOut]
                    for i in xrange(2, len(self.default_case)):
                        self.testCases[dir].append(self.default_case[i])
            if createFiles:
                self.writeTestcase()

if __name__ == "__main__":
    x = Problem('auction', 'D:/AMM2/Contests/SPOJ/Exams/auction/')
    print x.compare('', 'file.inp', 'file.out')
    print x.VALUE
    for key, value in x.testCases.iteritems():
        print key, value
    print x.subtask
    # x = problem('camera','D:/AMM2/Contests/TMP/camera/')
