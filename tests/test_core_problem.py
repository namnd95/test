import unittest
import utils
import os

import core.problem
import core.problem.config
import core.problem.functions
import core.problem.load_test_case
import core.problem.problem
import core.problem.test_case

PATH = os.path.dirname(__file__)
if len(PATH) == 0:
    PATH = '.'
PATH = PATH + '/test_core_problem/'


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


class TestLoadTestCase(unittest.TestCase):

    def check_test_case(self, test_case_1, test_case_2):
        self.assertEqual(test_case_1.id, test_case_2.id)
        self.assertTrue(
            (test_case_1.get_file_in() in test_case_2.get_file_in()) or
            (test_case_2.get_file_in() in test_case_1.get_file_in())
        )
        self.assertTrue(
            (test_case_1.get_file_out() in test_case_2.get_file_out()) or
            (test_case_2.get_file_out() in test_case_1.get_file_out())
        )

    def check_list_test_case(self, list_test_case_1, list_test_case_2):
        self.assertEqual(len(list_test_case_1), len(list_test_case_2))
        for i in xrange(len(list_test_case_1)):
            self.check_test_case(list_test_case_1[i], list_test_case_2[i])

    def test_load_themis_test_cases(self):
        self.check_list_test_case(
            [
                core.problem.test_case.TestCase(
                    'test1', 'divide.inp', 'divide.ans'
                ),
                core.problem.test_case.TestCase(
                    'test2', 'divide.inp', 'divide.ans'
                )
            ],
            core.problem.load_test_case.load_themis_test_cases(
                'divide', PATH + 'divide/'
            )
        )

    def test_load_normal_test_cases(self):
        self.check_list_test_case(
            [
                core.problem.test_case.TestCase('1', '1.in', '1.out'),
                core.problem.test_case.TestCase('2', '2.in', '2.out'),
                core.problem.test_case.TestCase('3', '3.in', '3.out')
            ],
            core.problem.load_test_case.load_normal_test_cases('divide', PATH + 'sum/')
        )


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestFunctions),
        unittest.TestLoader().loadTestsFromTestCase(TestLoadTestCase),
    ])


if __name__ == '__main__':
    utils.run(suite)
