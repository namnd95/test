import unittest

import utils
import test_core_compare
import test_core_test_case
import test_core_judge
import test_core_problem
import test_core_submission

import core
import core.compare
import core.test_case
import core.judge
import core.problem
import core.submission
import core.utils


def suite():
    compare_tests = test_core_compare.suite()
    test_case_tests = test_core_test_case.suite()
    problem_tests = test_core_problem.suite()
    submission_tests = test_core_submission.suite()
    judge_tests = test_core_judge.suite()
    return unittest.TestSuite([
        compare_tests, test_case_tests, judge_tests,
        problem_tests, submission_tests,
    ])

if __name__ == '__main__':
    utils.run(suite)
