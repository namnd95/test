import unittest

import config
import result
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


class TestCompareFile(unittest.TestCase):

    def test_word_ignore_space(self):
        self.assertEqual(
            config.get('word_ignore_space')('tests/1', 'tests/2').score, 1
        )
        self.assertEqual(
            config.get('word_ignore_space')('tests/1', 'tests/3').score, 0
        )

    def test_float_ignore_space(self):
        self.assertEqual(
            config.get('float_ignore_space')(
                'tests/1', 'tests/3', epsilon=1e-3).score,
            1
        )
        self.assertEqual(
            config.get('float_ignore_space')(
                'tests/1', 'tests/3', epsilon=1e-5).score,
            0
        )


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestFunction),
        unittest.TestLoader().loadTestsFromTestCase(TestCompareFile),
    ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
