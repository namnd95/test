import unittest

import utils
import test_core_compare
import test_core_problem
import test_core_submission
import test_core_judge

import core
import core.compare
import core.problem
import core.submission
import core.utils


def suite():
    compare_tests = test_core_compare.suite()
    problem_tests = test_core_problem.suite()
    submission_tests = test_core_submission.suite()
    judge_tests = test_core_judge.suite()
    return unittest.TestSuite([
        compare_tests, problem_tests, submission_tests, judge_tests
    ])

if __name__ == '__main__':
    utils.run(suite)
