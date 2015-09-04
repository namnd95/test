import unittest

import tests.test_core

import core


def suite():
    core_tests = tests.test_core.suite()
    return unittest.TestSuite([core_tests])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
