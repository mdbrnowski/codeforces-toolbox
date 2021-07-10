import json


def add_subcommand_config(subparsers):
    parser = subparsers.add_parser('config', help='change configuration of the cft')
    parser.set_defaults(func=config)


def config(args):
    print('Choose one of the following (type an integer):',
          '  1. change the template file', sep='\n')
    while (choice := input()) not in '1':
        pass
    choice = int(choice)

    if choice == 1:
        path = input('Path to the template: ')
        json.dump({'template': path}, open('cft_config.json', 'w'))
