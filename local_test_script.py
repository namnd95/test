import core
import core.utils

class ProblemSubmission:
    
    def __init__(self, problem, language, file):        
        self.problem = core.Problem(**problem)        
        
        result = core.make_submission(self.problem, language, file)
        print result.get_test_case_results()


prob_sub = core.utils.from_string(
    ProblemSubmission,
    file_name = 'local_test.json'
)
