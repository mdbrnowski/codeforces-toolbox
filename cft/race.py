import os
import shutil

TEMPLATE = r'path\_template.cpp'


def add_subcommand_race(subparsers):
    parser = subparsers.add_parser('race')
    parser.add_argument('contest', type=str, help='number of the contest')
    parser.set_defaults(func=race)


def race(args):
    contest = args.contest
    os.makedirs(contest)
    os.chdir(contest)
    for task in 'ABCDEFG':
        shutil.copy(TEMPLATE, f'{contest}{task}.cpp')
