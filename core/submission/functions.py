from string import Template

from core.compare import Result
import core.utils

from submission import Submission

COMPILE_PATH = '../../running_room/'
DATA_PATH = '../../running_room/data/'

# do not support subtasks and stop yet


def test_sequence(compare, run_command, test_cases,
                  subtasks=None, stop=False, **kargs):
    for test_case in testcases:
        # check test for stop
        # copy test case
        # run test
        # check test
        # remove test case
        # update stop for subtask
        pass


def get_params(problem):
    return dict(file=problem.id, problem=problem.id)


def make_submission(problem, language, file):
    # copy code
    core.utils.copy(file, COMPILE_PATH + problem.id)

    params = get_params(problem)
    result = Submission(problem, language)

    # compile code
    compile_result = core.utils.run_command(
        Template(problem.config.get_compile_command()).substitute(params),
        shell=True
    )

    if compile_result.get_exit_code() != 0:
        result.set_compile_result(compile_result.get_stderr())
    else:
        result.set_test_case_results(
            test_sequence(
                problem.compare,
                Template(problem.config.get_run_command()).substitute(params),
                problem.test_cases,
            )
        )

    return result
