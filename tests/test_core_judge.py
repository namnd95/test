import unittest
import os

import utils

import core.judge
import core.judge.config
from core.judge.functions import *

from core.compare.result import Result
from core.test_case import TestCase

PATH = os.path.dirname(__file__)
if len(PATH) == 0:
    PATH = '.'
PATH = os.path.join(PATH, 'test_core_compare')


class TestFunction(unittest.TestCase):

    def setUp(self):
        self.default_test_case = TestCase(
            'test', 'test.in', 'test.out',
            1.0, 256, 1
        )

    def test_sum(self):
        test_cases = [
            TestCase('1', '1.in', '1.out'),
            TestCase('2', '1.in', '1.out', score=2.5),
            TestCase('3', '1.in', '1.out', score=1.5),
        ]

        test_case_results = {
            '1': Result(1, 'a'),
            '2': Result(1, 'b'),
            '3': Result(0, 'c')
        }

        self.assertEqual(
            config.get('sum')(
                self.default_test_case,
                test_cases,
                test_case_results
            ),
            3.5
        )


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestFunction),
    ])

if __name__ == '__main__':
    utils.run(suite)
