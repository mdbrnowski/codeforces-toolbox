import json
import os
import sys

from sty import fg, rs

CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.codeforces-toolbox', 'cft_config.json')


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
