import unittest
import utils
import os

import core.problem
import core.problem.config
import core.problem.problem

from core.test_case import TestCase

PATH = os.path.dirname(__file__)
PATH = os.path.join(PATH, 'problems')

core.problem.config.default_config = core.utils.from_string(
    core.problem.config.ProblemConfig,
    file_name=os.path.join(PATH, 'config.json')
)


class TestProblemConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = core.problem.config.ProblemConfig(
            stdin=False, stdout=False, stop=False,
            language={
                "c++": {
                    'compile': 'g++ -g -std=c++0x $file -O2 -o "$problem\"',
                    "run": "$problem"
                }
            }
        )

    def setUp(self):
        self.config = TestProblemConfig.config

    def test_get_stdin(self):
        self.assertTrue(core.problem.config.default_config.get_stdin())
        self.assertFalse(self.config.get_stdin())

    def test_get_stdout(self):
        self.assertFalse(core.problem.config.default_config.get_stdout())
        self.assertFalse(self.config.get_stdout())

    def test_get_stop(self):
        self.assertTrue(core.problem.config.default_config.can_stop())
        self.assertFalse(self.config.can_stop())

    def test_get_compare_name(self):
        self.assertEqual(
            core.problem.config.default_config.get_compare_name(),
            'word_ignore_space'
        )

    def test_get_compare(self):
        self.assertEqual(
            core.problem.config.default_config.get_compare(),
            core.compare.config.get('word_ignore_space')
        )

    def test_get_judge_name(self):
        self.assertEqual(
            core.problem.config.default_config.get_judge_name(),
            'sum'
        )

    def test_get_judge(self):
        self.assertEqual(
            core.problem.config.default_config.get_judge(),
            core.judge.config.get('sum')
        )

    def test_get_compile_command(self):
        self.assertEqual(
            core.problem.config.default_config.get_compile_command('c++'),
            'g++ -g -std=c++0x $file  -o "$problem"'
        )
        self.assertEqual(
            core.problem.config.default_config.get_compile_command('pas'),
            'fpc -g $file  -o"$problem"'
        )

        self.assertEqual(
            self.config.get_compile_command('c++'),
            'g++ -g -std=c++0x $file -O2 -o "$problem"'
        )

        # Use default config
        self.assertEqual(
            self.config.get_compile_command('pas'),
            'fpc -g $file  -o"$problem"'
        )

    def test_get_run_command(self):
        self.assertEqual(
            core.problem.config.default_config.get_run_command('c++'),
            './$problem'
        )

        self.assertEqual(
            core.problem.config.default_config.get_run_command('pas'),
            '././$problem'
        )

        self.assertEqual(
            self.config.get_run_command('c++'),
            '$problem'
        )

        # Use default config
        self.assertEqual(
            self.config.get_run_command('pas'),
            '././$problem'
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
        unittest.TestLoader().loadTestsFromTestCase(TestProblemConfig),
        unittest.TestLoader().loadTestsFromTestCase(TestProblem),
    ])


if __name__ == '__main__':
    utils.run(suite)
