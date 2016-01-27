import unittest
import os

import utils

import core.compare
import core.compare.config
import core.compare.result
from core.compare.functions import *

from core.compare.result import Result


PATH = os.path.dirname(__file__)
if len(PATH) == 0:
    PATH = '.'
PATH = PATH + '/test_core_compare/'


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
            config.get('word_ignore_space')(
                PATH + '1', PATH + '2'
            ).get_score(), 1
        )
        self.assertEqual(
            config.get('word_ignore_space')(
                PATH + '1', PATH + '3'
            ).get_score(), 0
        )

    def test_float_ignore_space(self):
        self.assertEqual(
            config.get('float_ignore_space')(
                PATH + '1', PATH + '3', epsilon=1e-3).get_score(),
            1
        )
        self.assertEqual(
            config.get('float_ignore_space')(
                PATH + '1', PATH + '3', epsilon=1e-5).get_score(),
            0
        )


class TestResult(unittest.TestCase):

    def setUp(self):
        self.result = Result(1, 'OK')

    def test_get_score(self):
        self.assertEqual(self.result.get_score(), 1)
        self.assertNotEqual(self.result.get_score(), 1.5)

    def test_get_verdict(self):
        self.assertEqual(self.result.get_verdict(), 'OK')
        self.assertNotEqual(self.result.get_verdict(), 'ok')

    def test_equal(self):
        self.assertEqual(self.result, Result(1, 'OK'))
        self.assertNotEqual(self.result, Result(1, 'ok'))
        self.assertNotEqual(self.result, Result(2, 'OK'))
        self.assertFalse(self.result is None)
        self.assertFalse(self.result == 'abc')


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestFunction),
        unittest.TestLoader().loadTestsFromTestCase(TestCompareFile),
        unittest.TestLoader().loadTestsFromTestCase(TestResult),
    ])

if __name__ == '__main__':
    utils.run(suite)
