import json
import os
import sys

from sty import fg, rs


class Language:
    def __init__(self, n, name, extension):
        self.n = n    # value in CF submit request
        self.name = name
        self.ext = extension


CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.codeforces-toolbox', 'cft_config.json')

LANGUAGES = {
    '1': Language(50, 'GNU C++14', 'cpp'),
    '2': Language(54, 'GNU C++17', 'cpp'),
    '3': Language(61, 'GNU C++17 (64 bit)', 'cpp'),
    '4': Language(73, 'GNU C++20 (64 bit)', 'cpp'),
    '5': Language(59, 'Microsoft Visual C++ 2017', 'cpp'),
    '6': Language(43, 'GNU C11', 'c'),
    '7': Language(7,  'Python 2.7', 'py'),
    '8': Language(31, 'Python 3.8', 'py'),
    '9': Language(40, 'PyPy 2.7', 'py'),
    '10': Language(41, 'PyPy 3.7', 'py'),
    '11': Language(70, 'PyPy 3.7 (64 bit)', 'py'),
    '12': Language(36, 'Java 8', 'java'),
    '13': Language(60, 'Java 11', 'java'),
    '14': Language(72, 'Kotlin', 'kt'),
    '15': Language(75, 'Rust', 'rs'),
    '16': Language(9, 'C# Mono', 'cs'),
    '17': Language(65, 'C# .NET', 'cs'),
    '18': Language(32, 'Go', 'go')
}


def error_style(message) -> str:
    return fg(196) + message + rs.all   # red


def warning_style(message) -> str:
    return fg(220) + message + rs.all   # yellow


def info_style(message) -> str:
    return fg(244) + message + rs.all   # grey


def positive_style(message) -> str:
    return fg(70) + message + rs.all    # green


def negative_style(message) -> str:
    return fg(208) + message + rs.all   # orange


def neutral_style(message) -> str:
    return fg(69) + message + rs.all    # blue


def translate_problem_name(problem):
    if len(problem) <= 2:
        problem_letter = problem
        contest = os.path.basename(os.getcwd())
    else:
        if problem[-1].isnumeric():
            problem_letter = problem[-2:]
            contest = problem[:-2]
        else:
            problem_letter = problem[-1]
            contest = problem[:-1]
    return contest, problem_letter


def get_config(setting, strict=True):
    """
    :param setting: 'template', 'username', 'language', 'run', 'compile' or 'last_downloaded'
    :param strict: if the function should raise exception if not found
    :return: string or Language object
    """
    if setting == 'language':
        return _get_config_language(strict=strict)

    try:
        config_dict = json.load(open(CONFIG_FILE))
        setting = config_dict[setting]
    except FileNotFoundError:
        if not strict:
            return ''
        print(error_style('Configuration file has not been found. . Use `cft config`.'))
        sys.exit()
    except KeyError:
        if setting in ('compile', 'run') or not strict:
            return ''
        print(error_style(f'Specify your {setting} first.'))
        sys.exit()
    return setting


def _get_config_language(strict=True):
    try:
        config_dict = json.load(open(CONFIG_FILE))
        language = config_dict['language']
    except FileNotFoundError:
        if not strict:
            return Language(0, '', '')
        print(error_style('Configuration file has not been found. Use `cft config`.'))
        sys.exit()
    except KeyError:
        if not strict:
            return Language(0, '', '')
        print(error_style('Specify your programming language first.'))
        sys.exit()
    return Language(*language)


def set_config(setting, value):
    if not os.path.exists(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox')):
        os.makedirs(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox'))

    try:
        config_dict = json.load(open(CONFIG_FILE))
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        config_dict = dict()

    config_dict[setting] = value
    json.dump(config_dict, open(CONFIG_FILE, 'w'))
    return value
