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
                  subtasks=None, stop=False, display=None, **kargs):
    test_case_results = {}
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
            verdict = 'RE'
            if run_result.get_exit_code() in (1, -9):
                verdict = 'TLE'
            test_case_results[test_case.get_id()] = Result(0, verdict)
        else:
            test_case_results[test_case.get_id()] = compare(
                os.path.join(
                    DATA_PATH,
                    problem.default_test_case.get_file_out()
                ),
                test_case.get_file_out(problem)
            )

        if display is not None:
            display(test_case, test_case_results[test_case.get_id()])

        # remove test case
        core.utils.remove_file_in_directory(DATA_PATH)

        # TODO update stop for subtask
    return test_case_results


def get_params(file, problem):
    return dict(file=file, problem=problem.id)


def copy_file_to_compile_path(problem, language, file):
    file_name = os.path.join(
        COMPILE_PATH,
        os.path.basename(file)
    )

    core.utils.copy_file(file, file_name)
    return file_name


def compile_code(problem, language, file, params):
    compile_result = core.utils.run_process(
        Template(
            problem.config.get_compile_command(language)
        ).substitute(params),
        timelimit=30,
        cwd=COMPILE_PATH,
        shell=True
    )
    return compile_result


def make_submission(problem, language, file, display_compile=None, **kargs):
    compile_result = core.utils.RunResult(
        exit_code=2,
        stderr='No file'
    )

    try:
        # copy code
        params = get_params(os.path.basename(file), problem)
        copy_file_to_compile_path(problem, language, file)
        compile_result = compile_code(problem, language, file, params)
    except:
        pass

    if display_compile is not None:
        display_compile(compile_result)

    result = Submission(problem, language)
    if compile_result.get_exit_code() != 0:
        result.set_compile_message(compile_result.get_stderr())
    else:
        result.set_test_case_results(
            test_sequence(
                problem.config.get_compare(),
                Template(
                    problem.config.get_run_command(language)
                ).substitute(params),
                problem,
                **kargs
            )
        )

    result.set_score(problem.config.get_judge()(
        problem.default_test_case,
        problem.test_cases,
        result.get_test_case_results()
    ))
    core.utils.remove_file_in_directory(COMPILE_PATH)
    return result
