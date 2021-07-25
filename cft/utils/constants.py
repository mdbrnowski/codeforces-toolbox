import json
import os
import sys

from sty import fg, rs


class Language:
    def __init__(self, n, name, extension):
        self.n = n    # value in CF submit request
        self.name = name
        self.ext = extension


CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.codeforces-toolbox', 'cft_config.json')

LANGUAGES = {
    '1': Language(42, 'GNU G++11', 'cpp'),
    '2': Language(50, 'GNU G++14', 'cpp'),
    '3': Language(54, 'GNU G++17', 'cpp'),
    '4': Language(61, 'GNU G++17 (64 bit)', 'cpp'),
    '5': Language(2,  'Microsoft Visual C++ 2010', 'cpp'),
    '6': Language(59, 'Microsoft Visual C++ 2017', 'cpp'),
    '7': Language(43, 'GNU GCC C11', 'c')
}


def error_style(message):
    return fg(196) + message + rs.all   # red


def warning_style(message):
    return fg(220) + message + rs.all   # yellow


def positive_style(message):
    return fg(70) + message + rs.all    # green


def negative_style(message):
    return fg(208) + message + rs.all   # orange


def neutral_style(message):
    return fg(69) + message + rs.all    # blue


def translate_problem_name(problem):
    if len(problem) <= 2:
        problem_letter = problem
        contest = os.path.basename(os.getcwd())
    else:
        problem_letter = problem[4:]
        contest = problem[:4]
    return contest, problem_letter


def get_template():
    try:
        config_dict = json.load(open(CONFIG_FILE))
        template = config_dict['template']
    except FileNotFoundError:
        print(error_style('Configuration file has not been found.'))
        sys.exit()
    except KeyError:
        print(error_style('Specify your template file first.'))
        sys.exit()
    return template


def get_username():
    try:
        config_dict = json.load(open(CONFIG_FILE))
        username = config_dict['username']
    except FileNotFoundError:
        print(error_style('Configuration file has not been found.'))
        sys.exit()
    except KeyError:
        print(error_style('Specify your username first.'))
        sys.exit()
    return username


def get_language():
    try:
        config_dict = json.load(open(CONFIG_FILE))
        language = config_dict['language']
    except FileNotFoundError:
        print(error_style('Configuration file has not been found.'))
        sys.exit()
    except KeyError:
        print(error_style('Specify your programming language first.'))
        sys.exit()
    return Language(*language)


def get_compile_command():
    try:
        config_dict = json.load(open(CONFIG_FILE))
        compile_command = config_dict['compile']
    except FileNotFoundError:
        print(error_style('Configuration file has not been found.'))
        sys.exit()
    except KeyError:
        print(error_style('Specify compile command first.'))
        sys.exit()
    return compile_command
