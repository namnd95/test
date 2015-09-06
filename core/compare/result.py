class Result:

    def __init__(self, score, verdict):
        if len(verdict) > 128:
            verdict = ''

        self.score = score
        self.verdict = verdict

    def get_score(self):
        return self.score

    def get_verdict(self):
        return self.verdict
