import os
import sys
import unittest

import utils

import core.submission
import core.submission.submission
import core.submission.functions

from core.submission.submission import Submission
from core.compare.result import Result
from core.problem import Problem
import core.utils

TEST_PATH = os.path.dirname(__file__)
PATH = os.path.join(TEST_PATH, 'test_core_submission')


class TestSubmission(unittest.TestCase):

    def setUp(self):
        self.submission = Submission(None, None)

    def test_test_case_results(self):

        self.submission.set_test_case_results(
            {'1': Result(1, '1'), '2': Result(2, '2')}
        )

        self.assertEqual(
            {'1': Result(1, '1'), '2': Result(2, '2')},
            self.submission.get_test_case_results()
        )
        self.assertNotEqual(
            {'1': Result(1, '2'), '2': Result(2, '2')},
            self.submission.get_test_case_results()
        )

    def test_compile_messeage(self):
        self.submission.set_compile_message('ok')
        self.assertEqual(
            'ok',
            self.submission.get_compile_message()
        )
        self.assertNotEqual(
            'abc',
            self.submission.get_compile_message()
        )


@unittest.skipUnless(__name__ == '__main__' or '--all' in sys.argv, '')
class TestMakeSubmission(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PROBLEM_PATH = os.path.join(TEST_PATH, 'test_core_problem')
        cls.sum = Problem('sum', os.path.join(PROBLEM_PATH, 'sum'))
        cls.divide = Problem('divide', os.path.join(PROBLEM_PATH, 'divide'))

    def test_copy_and_compile_code(self):
        file = os.path.join(PATH, 'Full', 'sum.cpp')
        language = 'c++'
        problem = self.sum
        params = core.submission.functions.get_params(
            os.path.basename(file), problem
        )
        core.submission.functions.copy_file_to_compile_path(
            problem, language, file
        )
        compile_result = core.submission.functions.compile_code(
            problem, language, file, params
        )
        core.utils.remove_file_in_directory(
            core.submission.functions.COMPILE_PATH
        )
        if compile_result.get_exit_code() != 0:
            print compile_result.get_exit_code(), compile_result.get_stderr()
            self.assertTrue(False)

    def test_no_file(self):
        result = core.submission.functions.make_submission(
            self.sum, 'c++',
            'sum.cpp'
        )
        self.assertEqual(result.get_compile_message(), 'No file')

    def test_compile_error(self):
        result = core.submission.functions.make_submission(
            self.sum, 'c++',
            os.path.join(PATH, 'partial', 'sum.pas')
        )
        self.assertNotEqual(result.get_compile_message(), '')
        self.assertNotEqual(result.get_compile_message(), 'No file')

    def test_full_sum(self):
        result = core.submission.functions.make_submission(
            self.sum, 'c++',
            os.path.join(PATH, 'Full', 'sum.cpp')
        )
        self.assertEqual(
            result.get_test_case_results(),
            {
                '1': Result(1, 'AC'),
                '2': Result(1, 'AC'),
                '3': Result(1, 'AC')
            }
        )

    def test_partial_sum(self):
        result = core.submission.functions.make_submission(
            self.sum, 'c++',
            os.path.join(PATH, 'partial', 'sum.cpp')
        )
        self.assertEqual(
            result.get_test_case_results(),
            {
                '1': Result(0, 'Line 1 at 1 output -1 answer 3'),
                '2': Result(0, 'TLE'),
                '3': Result(0, 'RE')
            }
        )


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestSubmission),
        unittest.TestLoader().loadTestsFromTestCase(TestMakeSubmission),
    ])


if __name__ == '__main__':
    utils.run(suite)
