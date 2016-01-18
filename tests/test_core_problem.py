import unittest
import utils

import core.problem
import core.problem.config
import core.problem.functions
import core.problem.load_test_case
import core.problem.problem
import core.problem.test_case


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.file_out = ['abc.a', 'abc.out', 'abc.ans', 'output15.txt']
        self.file_inp = ['abc.in', 'abc.inp', 'input15.txt']
        self.other_file = [
            'test.c', 'test.cpp', 'test.pas', 'test.java', 'test.py',
            'test.exe', 'file.inp'
        ]

    def check_list(self, list, func, result):
        for item in list:
            self.assertEqual(func(item), result)

    def test_is_file_out(self):
        func = core.problem.functions.is_file_out

        self.check_list(self.file_out, func, True)
        self.check_list(self.file_inp, func, False)
        self.check_list(self.other_file, func, False)

    def test_is_file_in(self):
        func = core.problem.functions.is_file_in

        self.check_list(self.file_inp, func, True)
        self.check_list(self.file_out, func, False)        
        self.check_list(self.other_file, func, False)

    def test_is_other_file(self):
        func = core.problem.functions.is_other_file
        
        self.check_list(self.other_file, func, True)
        self.check_list(self.file_out, func, False)
        self.check_list(self.file_inp, func, False)        


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestFunctions),
    ])


if __name__ == '__main__':
    utils.run(suite)
