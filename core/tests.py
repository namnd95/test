import unittest

import compare.tests
import problem.tests

import compare
import problem
import utils


def suite():
    compare_tests = compare.tests.suite()
    return unittest.TestSuite([compare_tests])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
