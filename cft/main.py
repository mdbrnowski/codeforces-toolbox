#!/usr/bin/env python

import argparse

import requests

from cft import __version__
from cft.utils.config import config
from cft.utils.constants import *
from cft.utils.race import race
from cft.utils.submit import submit
from cft.utils.test import test
from cft.utils.upgrade import try_upgrade


def main():
    os.system('')    # enable colors in Windows cmd
    parser = argparse.ArgumentParser(prog='cft', description=neutral_style('----- Codeforces Toolbox -----'),
                                     epilog='Wish you high ratings!')
    parser.add_argument('-v', '--version', action='version', version=neutral_style(f'Codeforces Toolbox {__version__}'))
    subparsers = parser.add_subparsers()

    config_parser = subparsers.add_parser('config', help='change configuration of the cft')
    config_parser.set_defaults(func=config)

    race_parser = subparsers.add_parser('race', help='create folder and solution files based on template')
    race_parser.add_argument('contest', type=str, help='contest id')
    race_parser.set_defaults(func=race)

    test_parser = subparsers.add_parser('test', help='test solution file')
    test_parser.add_argument('problem', type=str, help='problem id in the form "A" or "1234A"')
    test_parser.add_argument('-d', '--download', action='store_true', help='force download test from CF')
    test_parser.add_argument('-p', '--precision', help='set precision for floating numbers, e.g. 1e-9')
    test_parser.set_defaults(func=test)

    submit_parser = subparsers.add_parser('submit', help='submit solution')
    submit_parser.add_argument('problem', type=str, help='problem id in the form "A" or "1234A"')
    submit_parser.set_defaults(func=submit)

    if sys.argv[1:]:
        args = parser.parse_args()
        try:
            args.func(args)
        except KeyboardInterrupt:
            print(info_style('\nAborted.'))
        except requests.RequestException:
            print(error_style('Something went wrong. Check your internet connection.'))
            sys.exit()
    else:
        parser.print_help()
        try_upgrade()
