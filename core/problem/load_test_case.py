from core.utils import get_list_file, get_list_dir

from functions import is_file_out, is_other_file
from test_case import TestCase


def load_themis_test_cases(id, directory):
    sub_dirs = get_list_dir(directory)
    test_cases = []
    for test_dir in sub_dirs:
        list_file = get_list_file(test_dir)[:2]
        file_in, file_out = list_file
        if is_file_out(file_in):
            file_in, file_out = file_out, file_in
        path = directory + '/' + test_dir + '/'
        test_cases.append(TestCase(
            id=test_dir,
            file_in=path + file_in,
            file_out=path + file_out
        ))
    return test_cases


def load_normal_test_cases(id, directory):
    list_file = get_list_file(directory)
    list_file_out = []
    list_file_in = []
    for file in list_file:
        if is_file_out(file):
            list_file_out.append(file)
        elif not is_other_file(file):
            list_file_in.append(file)

    list_file_in.sort()
    list_file_out.sort()

    test_cases = []
    path = directory + '/'
    for i in xrange(len(list_file_out)):
        file_in = list_file_in[i]
        file_out = list_file_out[i]
        test_cases.append(TestCase(
            id=file_in,
            file_in=path + file_in,
            file_out=path + file_out
        ))
    return test_cases
