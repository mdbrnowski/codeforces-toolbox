import json
import os
import sys

from sty import fg, rs

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cft_config.json')

error_style = fg.red
warning_style = fg.yellow
good_style = fg.li_green
bad_style = fg.yellow


def print_error(message):
    print(error_style + message + rs.all)


def print_warning(message):
    print(warning_style + message + rs.all)


def print_good(message):
    print(good_style + message + rs.all)


def print_bad(message):
    print(bad_style + message + rs.all)


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
        print_error('Configuration file has not been found.')
        sys.exit()
    except KeyError:
        print_error('Specify your template file first.')
        sys.exit()
    return template


def get_username():
    try:
        config_dict = json.load(open(CONFIG_FILE))
        username = config_dict['username']
    except FileNotFoundError:
        print_error('Configuration file has not been found.')
        sys.exit()
    except KeyError:
        print_error('Specify your username first.')
        sys.exit()
    return username


def get_compile_command():
    try:
        config_dict = json.load(open(CONFIG_FILE))
        compile_command = config_dict['compile']
    except FileNotFoundError:
        print_error('Configuration file has not been found.')
        sys.exit()
    except KeyError:
        print_error('Specify compile command first.')
        sys.exit()
    return compile_command
