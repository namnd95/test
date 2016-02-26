import sys

import core
import core.utils


def display(test_case, test_case_result):
    print 'Finish ' + test_case.__repr__()
    sys.stdout.flush()


def display_compile(compile_result):
    print 'Finish compile with exit code %d' % compile_result.get_exit_code()


class ProblemSubmission:

    def __init__(self, problem, language, file):
        self.problem = core.Problem(**problem)

        result = core.make_submission(
            self.problem, language, file,
            display_compile, display=display
        )

        print result.get_test_case_results()


prob_sub = core.utils.from_string(
    ProblemSubmission,
    file_name='local_test.json'
)
