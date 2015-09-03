import unittest

import core.tests

import core


def suite():
    core_tests = core.tests.suite()
    return unittest.TestSuite([core_tests])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
