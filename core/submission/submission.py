class Submission:

    def __init__(self, problem, language):
        self.problem = problem
        self.language = language

    def set_test_case_results(self, test_case_results):
        self.test_case_results = test_case_results

    def set_compile_message(self, compile_message):
        self.compile_message = compile_message

    def get_problem(self):
        return self.problem

    def get_language(self):
        return self.language

    def get_test_case_results(self):
        return self.test_case_results

    def get_compile_message(self):
        return self.compile_message
