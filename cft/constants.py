import os
import sys

from sty import fg, rs

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'cft_config.json')

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
