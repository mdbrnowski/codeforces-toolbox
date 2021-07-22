import getpass

import keyring

from .constants import *


def config(args):
    print('Choose one of the following (type an integer):',
          '  1. change the template file',
          '  2. change username and password',
          '  3. change password',
          '  4. set compile command',
          sep='\n')
    while (choice := input()) not in {'1', '2', '3', '4'}:
        print_warning('Type an integer 1, 2, 3 or 4:')
    choice = int(choice)

    try:
        config_dict = json.load(open(CONFIG_FILE))
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        config_dict = dict()

    print(CONFIG_FILE)
    if choice == 1:
        config_dict['template'] = input('Path to the template: ')
    if choice == 2:
        config_dict['username'] = input('Username: ')
    if choice in (2, 3):
        try:
            username = config_dict['username']
        except KeyError:
            print_error('First enter your username.')
            sys.exit()
        password = getpass.getpass('Password: ')
        keyring.set_password('codeforces-toolbox', username, password)
    if choice == 4:
        print('Set compile command, e.g. `g++ -Wall -O1`.\nIf you do not want to compile, just press enter.')
        config_dict['compile'] = input('Compile command: ')

    json.dump(config_dict, open(CONFIG_FILE, 'w'))
