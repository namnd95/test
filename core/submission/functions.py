from string import Template

from core.compare import Result
import core.utils

from submission import Submission

COMPILE_PATH = '../../running_room/'
DATA_PATH = '../../running_room/data/'

# do not support subtasks and stop yet


def test_sequence(compare, run_command, test_cases,
                  subtasks=None, stop=False, **kargs):
    test_case_results = []
    for test_case in testcases:
        # TODO check test for stop
        # copy test
        core.utils.copy(
            test_case.get_file_in(),
            DATA_PATH + problem.default_test_case.get_file_in()
        )

        # run test
        file_in = None
        file_out = None
        if problem.config.get_stdin():
            file_in = problem.default_test_case.get_file_in()
        if problem.config.get_stdout():
            file_out = problem.default_test_case.get_file_out()
        run_result = core.utils.run_command(
            run_command,
            file_in=file_in,
            file_out=file_out,
            cwd=DATA_PATH
        )

        # check test
        if run_result.get_exit_code() != 0:
            test_case_results.append(Result(0, 'RE'))
        else:
            test_case_results.append(compare(
                DATA_PATH + problem.default_test_case.get_file_out(),
                test_case.get_file_out()
            ))

        # remove test case
        core.utils.remove_file_in_directory(DATA_PATH)

        # TODO update stop for subtask


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
                problem.config.get_compare(),
                Template(problem.config.get_run_command()).substitute(params),
                problem.test_cases,
            )
        )

    return result
