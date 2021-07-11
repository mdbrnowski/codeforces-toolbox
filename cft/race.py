import os
import shutil
import sys
import json
from colorama import init as colorama_init
from termcolor import cprint

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'cft_config.json')

try:
    config_dict = json.load(open(CONFIG_FILE))
    template = config_dict['template']
except (FileNotFoundError, KeyError):
    template = ''


def add_subcommand_race(subparsers):
    parser = subparsers.add_parser('race', help='create folder and solution files based on the template')
    parser.add_argument('contest', type=str, help='contest id')
    parser.set_defaults(func=race)


def race(args):
    colorama_init()
    if not os.path.exists(template):
        cprint('Template does not exist', 'red', 'on_white')
        sys.exit()
    contest = args.contest
    os.makedirs(contest)
    os.chdir(contest)
    for task in 'ABCDEFG':
        os.makedirs(task)
        os.chdir(task)
        shutil.copy(template, f'{contest}{task}.cpp')
        os.chdir('..')
