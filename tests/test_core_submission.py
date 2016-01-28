import unittest

import utils

import core.submission
import core.submission.submission
import core.submission.functions

from core.submission.submission import Submission
from core.compare.result import Result


class TestSubmission(unittest.TestCase):

    def setUp(self):
        self.submission = Submission(None, None)

    def test_test_case_results(self):

        self.submission.set_test_case_results(
            [Result(1, '1'), Result(2, '2')]
        )

        self.assertEqual(
            [Result(1, '1'), Result(2, '2')],
            self.submission.get_test_case_results()
        )
        self.assertNotEqual(
            [Result(1, '2'), Result(2, '2')],
            self.submission.get_test_case_results()
        )

    def test_compile_messeage(self):
        self.submission.set_compile_message('ok')
        self.assertEqual(
            'ok',
            self.submission.get_compile_message()
        )
        self.assertNotEqual(
            'abc',
            self.submission.get_compile_message()
        )


def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestSubmission),
    ])


if __name__ == '__main__':
    utils.run(suite)
