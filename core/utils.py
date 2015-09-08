import os
import shutil
import subprocess
import time
from threading import Timer
import signal
import json


class RunResult:

    def __init__(self, time=0.00, memory=0.00, exit_code=0, stderr=''):
        self.time = time
        self.memory = memory
        self.exit_code = exit_code
        self.stderr = stderr

    def get_running_time(self):
        return self.time

    def get_running_memory(self):
        return self.memory

    def get_exit_code(self):
        return self.exit_code

    def get_stderr(self):
        return self.stderr


def run_process(command, timelimit=1000, memlimit=1024,
                file_in=None, file_out=None, **kargs):

    class Alarm(Exception):
        pass

    def alarm_handler(signum, frame):
        raise Alarm

    # init stdin and stdout
    fi = None
    fo = subprocess.PIPE
    if file_in is not None:
        fi = open(file_in, 'r')
    if file_out is not None:
        fo = open(file_out, 'w')

    process = subprocess.Popen(command, stdin=fi, stdout=fo,
                               stderr=subprocess.PIPE, **kagrs)

    kill_proc = lambda p: p.terminate()
    timer = Timer(timelimit, kill_proc, [process])
    timer.start()
    stdout, stderr = process.communicate()
    timer.cancel()

    # close file if redirect stdin and stdout
    if file_in is not None:
        fi.close()
    if file_out is not None:
        fo.close()

    return RunResult(exit_code=process.returncode, stderr=stdout + stderr)


def get_list_file(directory):
    return os.walk(directory).next()[2]


def get_list_dir(directory):
    return os.walk(directory).next()[1]


def copy_file(src, dst):
    shutil.copyfile(src, dst)


def remove_file_in_directory(directory):
    for file in get_list_file(directory):
        file_path = os.path.join(directory, file)
        os.unlink(file_path)


def get_name_part(file_name):
    seperation_index = file_name.rfind('.')
    if seperation_index == -1:
        return file_name
    else:
        return file_name[:seperation_index]


def from_string(cls, s):
    return cls(**json.loads(s))


def to_string(obj):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__)
