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


class TestTestCase(unittest.TestCase):

    def setUp(self):
        self.default_test_case = core.problem.test_case.TestCase(
            'test', 'test.in', 'test.out',
            1.0, 256, 1
        )
        self.test_case = core.problem.test_case.TestCase(
            'test2', 'test2.inp', 'test2.ans'
        )

    def test_get_id(self):
        self.assertEqual(self.default_test_case.get_id(), 'test')
        self.assertEqual(self.test_case.get_id(), 'test2')

    def test_get_file_in(self):
        self.assertEqual(self.default_test_case.get_file_in(), 'test.in')
        self.assertEqual(self.test_case.get_file_in(), 'test2.inp')

    def test_get_file_out(self):
        self.assertEqual(self.default_test_case.get_file_out(), 'test.out')
        self.assertEqual(self.test_case.get_file_out(), 'test2.ans')

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
            core.problem.test_case.TestCase(
                'test', 'test.in', 'test.out',
                1.0, 256, 1
            )
        )
        
        self.assertEqual(
            self.test_case,
            core.problem.test_case.TestCase(
                'test2', 'test2.inp', 'test2.ans'
            )
        )
        
    def test_not_equal(self):
        self.assertNotEqual(
            self.default_test_case,
            core.problem.test_case.TestCase(
                'test', 'test.inp', 'test.out',
                1.0, 256, 1
            )
        )

        self.assertNotEqual(
            self.test_case,
            core.problem.test_case.TestCase(
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


class TestProblemConfig(unittest.TestCase):

    def setUp(self):
        self.default_config = core.problem.config.ProblemConfig(
            stdin=True,
            stdout=False,
            stop=True,
            language={
                'c++': {
                    'compile': 'g++ -g -std=gnu++11 $file  -o "$problem"',
                    'run': '$problem',
                },

                'pas': {
                    'compile': 'fpc -g $file  -o"$problem"',
                    'run': './$problem',
                },
            }
        )

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


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestTestCase),
        unittest.TestLoader().loadTestsFromTestCase(TestFunctions),
        unittest.TestLoader().loadTestsFromTestCase(TestLoadTestCase),
        unittest.TestLoader().loadTestsFromTestCase(TestProblemConfig),
    ])


if __name__ == '__main__':
    utils.run(suite)
