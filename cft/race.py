import os
import shutil
import sys
from colorama import init as colorama_init
from termcolor import cprint


TEMPLATE = r'path\_template.cpp'


def add_subcommand_race(subparsers):
    parser = subparsers.add_parser('race', help='create folder and solution files based on the template')
    parser.add_argument('contest', type=str, help='contest id')
    parser.set_defaults(func=race)


def race(args):
    colorama_init()
    if not os.path.exists(TEMPLATE):
        cprint('Template does not exist', 'red', 'on_white')
        sys.exit()
    contest = args.contest
    os.makedirs(contest)
    os.chdir(contest)
    for task in 'ABCDEFG':
        os.makedirs(task)
        os.chdir(task)
        shutil.copy(TEMPLATE, f'{contest}{task}.cpp')
        os.chdir('..')
