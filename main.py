import argparse
from cft.race import add_subcommand_race
from cft.submit import add_subcommand_submit
from cft.test import add_subcommand_test

parser = argparse.ArgumentParser(prog='cft', description='Codeforces tool', epilog='Wish you high ratings!')

subparsers = parser.add_subparsers(help='command')

add_subcommand_race(subparsers)
add_subcommand_submit(subparsers)
add_subcommand_test(subparsers)

args = parser.parse_args()

args.func(args)
