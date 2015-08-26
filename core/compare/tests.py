import unittest
from functions import *


class TestFunction(unittest.TestCase):

    def test_equal(self):
        self.assertTrue(equal('12', '12'))
        self.assertFalse(equal('12', '13'))

    def test_float_equal(self):
        self.assertTrue(equal_with_epsilon('1.0000001', '1.0000002'))
        self.assertFalse(equal_with_epsilon('1.0001', '1.0002'))

        self.assertTrue(equal_with_epsilon('1.0001', '1.0002', epsilon=1e-3))
        self.assertFalse(equal_with_epsilon('1.0001', '1.0002', epsilon=1e-5))

    def test_compare_line_ignore_space(self):
        self.assertIsNone(compare_line_ignore_space(
            1, '1 2 3 4', '1 2 3 4', equal
        ))
        self.assertIsNotNone(compare_line_ignore_space(
            1, '1 2 3 4.001', '1 2 3 4', equal
        ))
        self.assertIsNone(compare_line_ignore_space(
            1, '1 2 3 4.001', '1 2 3 4', equal_with_epsilon, epsilon=0.01
        ))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFunction)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
