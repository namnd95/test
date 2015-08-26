import unittest
import compare.tests


def suite():
    compare_tests = compare.tests.suite()
    return unittest.TestSuite([compare_tests])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
