import os
import shutil
import sys
import json
from termcolor import cprint
from .constants import CONFIG_FILE

try:
    config_dict = json.load(open(CONFIG_FILE))
    template = config_dict['template']
except (FileNotFoundError, KeyError):
    template = ''


def race(args):
    contest = args.contest
    if not os.path.exists(template):
        cprint('Template does not exist', 'red', 'on_white')
        sys.exit()
    os.makedirs(contest)
    os.chdir(contest)
    for problem_letter in contest_letters(contest):
        shutil.copy(template, f'{contest}{problem_letter}.cpp')


def contest_letters (contest):
    return 'ABCDEFG'
    # TODO: make this work