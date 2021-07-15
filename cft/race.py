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
    if not os.path.exists(template):
        cprint('Template does not exist', 'red', 'on_white')
        sys.exit()
    contest = args.contest
    os.makedirs(contest)
    os.chdir(contest)
    for problem_letter in 'ABCDEFG':
        os.makedirs(problem_letter)
        os.chdir(problem_letter)
        shutil.copy(template, f'{contest}{problem_letter}.cpp')
        os.chdir('..')
