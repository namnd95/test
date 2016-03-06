import config


def sum(default_test_case, test_cases, test_case_results, **kargs):
    score = 0
    for test_case in test_cases:
        test_result = test_case_results.get(test_case.get_id())
        test_score = 0
        if test_result is not None:
            test_score = test_result.get_score()
        score = score + test_score * test_case.get_score(default_test_case)
    return score

config.update(sum)
