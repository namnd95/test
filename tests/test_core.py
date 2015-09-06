import unittest

import utils
import test_core_compare
import test_core_problem

import core
import core.compare
import core.problem
import core.utils


def suite():
    compare_tests = test_core_compare.suite()
    return unittest.TestSuite([compare_tests])

if __name__ == '__main__':
    utils.run(suite)
