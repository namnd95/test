from core.utils import get_list_file, get_list_dir, get_name_part

from functions import is_file_out, is_other_file, is_file_in
from test_case import TestCase


def load_themis_test_cases(id, directory):
    sub_dirs = get_list_dir(directory)
    test_cases = []
    for test_dir in sub_dirs:
        path = directory + '/' + test_dir + '/'
        list_file = get_list_file(path)[:2]
        file_in, file_out = list_file
        if is_file_out(file_in):
            file_in, file_out = file_out, file_in
        test_cases.append(TestCase(
            id=test_dir,
            file_in=test_dir + '/' + file_in,
            file_out=test_dir + '/' + file_out
        ))
    return test_cases


def load_normal_test_cases(id, directory):
    list_file = get_list_file(directory)
    list_file_out = []
    list_file_in = []
    for file in list_file:
        if is_file_out(file):
            list_file_out.append(file)
        elif is_file_in(file):
            list_file_in.append(file)

    list_file_in.sort()
    list_file_out.sort()

    test_cases = []
    for i in xrange(len(list_file_out)):
        file_in = list_file_in[i]
        file_out = list_file_out[i]
        test_cases.append(TestCase(
            id=get_name_part(file_in),
            file_in=file_in,
            file_out=file_out
        ))
    return test_cases
