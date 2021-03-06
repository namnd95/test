import os


class TestCase:

    def __init__(self,
                 id, file_in, file_out,
                 time_limit=None, mem_limit=None, score=None):
        self.id = id
        self.file_in = file_in
        self.file_out = file_out
        self.time_limit = time_limit
        self.mem_limit = mem_limit
        self.score = score

    def get_id(self):
        return self.id

    def get_file_in(self, problem=None):
        if problem is None:
            return self.file_in
        else:
            return os.path.join(problem.directory, self.file_in)

    def get_file_out(self, problem=None):
        if problem is None:
            return self.file_out
        else:
            return os.path.join(problem.directory, self.file_out)

    def get_time_limit(self, default_test_case=None):
        if self.time_limit is not None:
            return self.time_limit
        else:
            return default_test_case.time_limit

    def get_mem_limit(self, default_test_case=None):
        if self.mem_limit is not None:
            return self.mem_limit
        else:
            return default_test_case.mem_limit

    def get_score(self, default_test_case=None):
        if self.score is not None:
            return self.score
        else:
            return default_test_case.score

    def __repr__(self):
        return self.id + ' ' + self.file_in + ' ' + self.file_out

    def __eq__(self, other):
        return self.id == other.id and \
            self.file_in == other.file_in and \
            self.file_out == other.file_out
