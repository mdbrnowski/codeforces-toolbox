import argparse
from race import add_subcommand_race
from submit import add_subcommand_submit

parser = argparse.ArgumentParser(prog='cft', description='Codeforces tool', epilog='Wish you high ratings!')

subparsers = parser.add_subparsers(help='command')

add_subcommand_race(subparsers)
add_subcommand_submit(subparsers)

args = parser.parse_args()

args.func(args)
