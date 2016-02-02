import unittest
import utils
import os

import core.problem
import core.problem.config
import core.problem.functions
import core.problem.load_test_case
import core.problem.problem
from core.problem.test_case import TestCase

PATH = os.path.dirname(__file__)
PATH = os.path.join(PATH, 'test_core_problem')


class TestTestCase(unittest.TestCase):

    def setUp(self):
        self.default_test_case = TestCase(
            'test', 'test.in', 'test.out',
            1.0, 256, 1
        )
        self.test_case = TestCase(
            'test2', 'test2.inp', 'test2.ans'
        )
        self.sum = core.problem.problem.Problem(
            'sum', os.path.join(PATH, 'sum'))
        self.divide = core.problem.problem.Problem(
            'divide', os.path.join(PATH, 'divide'))

    def test_get_id(self):
        self.assertEqual(self.default_test_case.get_id(), 'test')
        self.assertEqual(self.test_case.get_id(), 'test2')

    def test_get_file_in(self):
        self.assertEqual(self.default_test_case.get_file_in(), 'test.in')
        self.assertEqual(self.test_case.get_file_in(), 'test2.inp')
        self.assertEqual(
            self.sum.test_cases[0].get_file_in(self.sum),
            os.path.join(PATH, 'sum', '1.in')
        )
        self.assertEqual(
            self.divide.test_cases[0].get_file_in(self.divide),
            os.path.join(PATH, 'divide', 'test1', 'divide.inp')
        )

    def test_get_file_out(self):
        self.assertEqual(self.default_test_case.get_file_out(), 'test.out')
        self.assertEqual(self.test_case.get_file_out(), 'test2.ans')
        self.assertEqual(
            self.sum.test_cases[0].get_file_out(self.sum),
            os.path.join(PATH, 'sum', '1.out')
        )
        self.assertEqual(
            self.divide.test_cases[0].get_file_out(self.divide),
            os.path.join(PATH, 'divide', 'test1', 'divide.ans')
        )

    def test_get_time_limit(self):
        self.assertAlmostEqual(self.default_test_case.get_time_limit(), 1.0)
        self.assertAlmostEqual(
            self.test_case.get_time_limit(self.default_test_case), 1.0
        )

    def test_get_mem_limit(self):
        self.assertAlmostEqual(self.default_test_case.get_mem_limit(), 256)
        self.assertAlmostEqual(
            self.test_case.get_mem_limit(self.default_test_case), 256
        )

    def test_get_score(self):
        self.assertAlmostEqual(self.default_test_case.get_score(), 1.0)
        self.assertAlmostEqual(
            self.test_case.get_score(self.default_test_case), 1.0
        )

    def test_equal(self):
        self.assertEqual(
            self.default_test_case,
            TestCase(
                'test', 'test.in', 'test.out',
                1.0, 256, 1
            )
        )

        self.assertEqual(
            self.test_case,
            TestCase(
                'test2', 'test2.inp', 'test2.ans'
            )
        )

    def test_not_equal(self):
        self.assertNotEqual(
            self.default_test_case,
            TestCase(
                'test', 'test.inp', 'test.out',
                1.0, 256, 1
            )
        )

        self.assertNotEqual(
            self.test_case,
            TestCase(
                'test2', 'test2.inp', 'test2.out'
            )
        )


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

    def test_load_themis_test_cases(self):
        self.assertEqual(
            [
                TestCase(
                    'test1',
                    os.path.join('test1', 'divide.inp'),
                    os.path.join('test1', 'divide.ans')
                ),
                TestCase(
                    'test2',
                    os.path.join('test2', 'divide.inp'),
                    os.path.join('test2', 'divide.ans')
                )
            ],
            core.problem.load_test_case.load_themis_test_cases(
                'divide', os.path.join(PATH, 'divide')
            )
        )

    def test_load_normal_test_cases(self):
        self.assertEqual(
            [
                TestCase('1', '1.in', '1.out'),
                TestCase('2', '2.in', '2.out'),
                TestCase('3', '3.in', '3.out')
            ],
            core.problem.load_test_case.load_normal_test_cases(
                'divide', os.path.join(PATH, 'sum')
            )
        )


class TestProblemConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.default_config = core.utils.from_string(
            core.problem.config.ProblemConfig,
            file_name=os.path.join(PATH, 'config.json')
        )

    def setUp(self):
        self.default_config = TestProblemConfig.default_config

    def test_get_stdin(self):
        self.assertTrue(self.default_config.get_stdin())

    def test_get_stdout(self):
        self.assertFalse(self.default_config.get_stdout())

    def test_get_stop(self):
        self.assertTrue(self.default_config.can_stop())

    def test_get_compile_command(self):
        self.assertEqual(
            self.default_config.get_compile_command('c++'),
            'g++ -g -std=gnu++11 $file  -o "$problem"'
        )
        self.assertEqual(
            self.default_config.get_compile_command('pas'),
            'fpc -g $file  -o"$problem"'
        )

    def test_get_run_command(self):
        self.assertEqual(
            self.default_config.get_run_command('c++'),
            '$problem'
        )

        self.assertEqual(
            self.default_config.get_run_command('pas'),
            './$problem'
        )


class TestProblem(unittest.TestCase):

    def setUp(self):
        self.sum = core.problem.problem.Problem(
            'sum', os.path.join(PATH, 'sum')
        )
        self.divide = core.problem.problem.Problem(
            'divide', os.path.join(PATH, 'divide')
        )

    def test_read_config(self):
        self.assertFalse(self.divide.config.get_stdin())
        self.assertFalse(self.divide.config.get_stdout())
        self.assertFalse(self.divide.config.can_stop())

    def test_problem_test_cases(self):
        self.assertEqual(
            self.sum.test_cases,
            [
                TestCase('1', '1.in', '1.out'),
                TestCase('2', '2.in', '2.out'),
                TestCase('3', '3.in', '3.out'),
            ]
        )

        self.assertEqual(
            self.divide.test_cases,
            [
                TestCase(
                    'test1',
                    os.path.join('test1', 'divide.inp'),
                    os.path.join('test1', 'divide.ans')
                ),
                TestCase(
                    'test2',
                    os.path.join('test2', 'divide.inp'),
                    os.path.join('test2', 'divide.ans')
                )
            ]
        )


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestTestCase),
        unittest.TestLoader().loadTestsFromTestCase(TestFunctions),
        unittest.TestLoader().loadTestsFromTestCase(TestLoadTestCase),
        unittest.TestLoader().loadTestsFromTestCase(TestProblemConfig),
        unittest.TestLoader().loadTestsFromTestCase(TestProblem),
    ])


if __name__ == '__main__':
    utils.run(suite)
