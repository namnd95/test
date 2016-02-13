import os
import subprocess
import time
from threading import Timer
import signal

"""
    Use this
    Language
    Judge
"""


def getListFile(directory):
    return os.walk(directory).next()[2]


def getListDir(directory):
    return os.walk(directory).next()[1]


def run_process(command, timelimit=1000, memlimit=1024,
                FileIn=None, FileOut=None, shell=False):

    class Alarm(Exception):
        pass

    def alarm_handler(signum, frame):
        raise Alarm

    # init stdin and stdout
    fi = None
    fo = subprocess.PIPE
    if FileIn is not None:
        fi = open(FileIn, 'r')
    if FileOut is not None:
        fo = open(FileOut, 'w')

    process = subprocess.Popen(command, stdin=fi, stdout=fo,
                               stderr=subprocess.PIPE, shell=shell)

    kill_proc = lambda p: p.terminate()
    timer = Timer(timelimit, kill_proc, [process])
    timer.start()
    stdout, stderr = process.communicate()
    timer.cancel()

    # close file if redirect stdin and stdout
    if (FileIn is not None):
        fi.close()
    if (FileOut is not None):
        fo.close()

    return stdout, stderr, process.returncode

if __name__ == "__main__":
    print run_process('notepad', 2)
    print signal.getsignal(signal.SIGTERM)
