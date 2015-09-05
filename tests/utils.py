import unittest
import sys

sys.path.append('..')


def run(suite):
    unittest.TextTestRunner(verbosity=2).run(suite())
