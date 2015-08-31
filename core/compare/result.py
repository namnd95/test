class Result:

    def __init__(self, score, verdict):
        if len(verdict) > 128:
            verdict = ''

        self.score = score
        self.verdict = verdict

    def getScore(self):
        return self.score

    def getVerdict(self):
        return self.verdict
