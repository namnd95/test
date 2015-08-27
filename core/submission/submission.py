class Submission:

    def __init__(self, problem, language, test_case_results):
        self.problem = problem
        self.language = language
        self.test_case_results = test_case_results

    def get_problem(self):
        return self.problem

    def get_language(self):
        return self.language

    def get_test_case_results(self):
        return self.test_case_results
