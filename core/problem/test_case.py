class TestCase:

    def __init__(self, id, file_in, file_out, time_limit, mem_limit, score):
        self.id = id
        self.file_in = file_in
        self.file_out = file_out
        self.time_limit = time_limit
        self.mem_limit = mem_limit
        self.score = score

    def get_id(self):
        return self.id

    def get_file_in(self):
        return self.file_in

    def get_file_out(self):
        return self.file_out

    def get_time_limit(self):
        return self.time_limit

    def get_mem_limit(self):
        return self.mem_limit

    def get_score(self):
        return self.score
