import config


def sum(default_test_case, test_cases, test_case_results, **kargs):
    score = 0
    for test_case in test_cases:
        test_score = test_case_results.get(test_case.get_id(), 0)
        score = score + test_score * test_case.get_score(default_test_case)
    return score

config.update(sum)
