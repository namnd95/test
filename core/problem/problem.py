from core.utils import get_list_file, get_list_dir

from functions import is_file_out, is_other_file
from config import ProblemConfig, default_config
from test_case import TestCase
from load_test_case import load_themis_test_cases, load_normal_test_cases


class Problem:

    def __init__(self, id, directory):
        self.id = id
        self.directory = directory
        self.default_test_case = TestCase(
            'default',
            id + '.inp',
            id + '.out',
            time_limit=1.5,
            mem_limit=1024,
            score=1
        )
        self.load_config()
        self.load_test_cases()

    def load_config(self):
        try:
            self.read_config()
        except:
            self.config = default_config.copy()

        if not self.config.language:
            self.config.language = default_config.language

    def read_config(self):
        raise

    def load_test_cases(self):
        try:
            self.read_test_cases()
        except:
            self.auto_load_test_cases()

    def read_test_cases(self):
        raise

    def auto_load_test_cases(self, contest_style=None):
        if contest_style is None:
            sub_dirs = get_list_dir(self.directory)
            if sub_dirs:
                contest_style = 'themis'
            else:
                contest_style = 'normal'

        if contest_style == 'themis':
            self.test_cases = load_themis_test_cases(self.id, self.directory)
        else:
            self.test_cases = load_normal_test_cases(self.id, self.directory)
