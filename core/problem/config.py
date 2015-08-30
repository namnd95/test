import copy
import json


class Language:

    def __init__(self, name='', compile='', run='', **kargs):
        self.compile = compile
        self.run = run

    def get_compile_command(self):
        return self.compile

    def get_run_command(self):
        return self.run


class ProblemConfig:

    def __init__(self, stdin=True, stdout=True, stop=False,
                 language={}, **kargs):
        self.stdin = stdin
        self.stdout = stdout
        self.stop = stop
        self.language = {}
        for key, value in language.iteritems():
            self.language[key] = Language(**value)

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

    @classmethod
    def from_string(cls, s):
        return cls(**json.loads(s))

    def copy(self):
        return copy.deepcopy(self)

    def get_stdin(self):
        return self.stdin

    def get_stdout(self):
        return self.stdout

    def can_stop(self):
        return self.stop

    def get_language(self):
        return self.language

    def get_compile_command(self, language):
        return self.language[language].get_compile_command()

    def get_run_command(self, language):
        return self.language[language].get_run_command()


default_config = ProblemConfig(
    stdin=True,
    stdout=True,
    language={
        'c++': {
            'compile': 'g++ -g -Wall  -Wl,--stack=268435456 -std=gnu++11 $file  -o "$problem"',
            'run': '$problem',
        },
    }
)
