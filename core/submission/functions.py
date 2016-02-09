import os
from string import Template

from core.compare import Result
import core.utils

from submission import Submission

PATH = os.path.join(os.path.dirname(__file__), '..', '..')
COMPILE_PATH = os.path.join(PATH, 'RunningRoom')
DATA_PATH = os.path.join(COMPILE_PATH, 'data')

# do not support subtasks and stop yet


def test_sequence(compare, run_command, problem,
                  subtasks=None, stop=False, **kargs):
    test_case_results = []
    for test_case in problem.test_cases:
        # TODO check test for stop
        # copy test
        core.utils.copy_file(
            test_case.get_file_in(problem),
            os.path.join(DATA_PATH, problem.default_test_case.get_file_in())
        )

        # run test
        file_in = None
        file_out = None
        if problem.config.get_stdin():
            file_in = problem.default_test_case.get_file_in()
        if problem.config.get_stdout():
            file_out = problem.default_test_case.get_file_out()
        run_result = core.utils.run_process(
            os.path.join(COMPILE_PATH, run_command),
            file_in=file_in,
            file_out=file_out,
            cwd=DATA_PATH
        )

        # check test
        if run_result.get_exit_code() != 0:
            test_case_results.append(Result(0, 'RE'))
        else:
            test_case_results.append(
                compare(
                    os.path.join(
                        DATA_PATH,
                        problem.default_test_case.get_file_out()
                    ),
                    test_case.get_file_out(problem)
                )
            )

        # remove test case
        core.utils.remove_file_in_directory(DATA_PATH)

        # TODO update stop for subtask
    return test_case_results


def get_params(file, problem):
    return dict(file=file, problem=problem.id)


def make_submission(problem, language, file):
    # copy code
    core.utils.copy_file(
        file,
        os.path.join(
            COMPILE_PATH,
            os.path.basename(file)
        )
    )

    params = get_params(os.path.basename(file), problem)
    result = Submission(problem, language)

    # compile code
    compile_result = core.utils.run_process(
        Template(
            problem.config.get_compile_command(language)
        ).substitute(params),
        cwd=COMPILE_PATH,
        shell=True
    )

    if compile_result.get_exit_code() != 0:
        result.set_compile_message(compile_result.get_stderr())
    else:
        result.set_test_case_results(
            test_sequence(
                problem.config.get_compare(),
                Template(
                    problem.config.get_run_command(language)
                ).substitute(params),
                problem
            )
        )

    return result
