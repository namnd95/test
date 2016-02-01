import copy
import os

import core.utils


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
        try:
            return self.language[language].get_compile_command()
        except:
            if language in default_config.language:
                return default_config.language[language].get_compile_command()
            else:
                return ''

    def get_run_command(self, language):
        try:
            return self.language[language].get_run_command()
        except:
            if language in default_config.language:
                return default_config.language[language].get_run_command()
            else:
                return ''


PATH = os.path.dirname(__file__)
default_config = core.utils.from_string(
    ProblemConfig,
    file_name=os.path.join(PATH, 'config.json')
)
