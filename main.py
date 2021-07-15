import argparse
from colorama import init as colorama_init
from cft.config import config
from cft.race import race
from cft.test import test
from cft.submit import submit

colorama_init()

parser = argparse.ArgumentParser(prog='cft', description='Codeforces tool', epilog='Wish you high ratings!')

subparsers = parser.add_subparsers()

config_parser = subparsers.add_parser('config', help='change configuration of the cft')
config_parser.set_defaults(func=config)

race_parser = subparsers.add_parser('race', help='create folder and solution files based on the template')
race_parser.add_argument('contest', type=str, help='contest id')
race_parser.set_defaults(func=race)

test_parser = subparsers.add_parser('test', help='test solution file')
test_parser.add_argument('problem', type=str, help='problem id in the form "A" or "1234A"')
test_parser.set_defaults(func=test)

submit_parser = subparsers.add_parser('submit', help='submit solution')
submit_parser.add_argument('problem', type=str, help='problem id in the form "A" or "1234A"')
submit_parser.set_defaults(func=submit)

args = parser.parse_args()

args.func(args)
