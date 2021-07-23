import getpass
import sys

import keyring

from .constants import *


def config(args):
    print('Choose one of the following (type an integer):',
          '  1. change the template file',
          '  2. change username and password',
          '  3. change password',
          '  4. set compile command',
          sep='\n')
    try:
        while (choice := input()) not in {'1', '2', '3', '4'}:
            print(warning_style('Type an integer 1, 2, 3 or 4:'))
        choice = int(choice)
    except KeyboardInterrupt:
        print(warning_style('Aborted.'))
        sys.exit()

    if not os.path.exists(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox')):
        os.makedirs(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox'))

    try:
        config_dict = json.load(open(CONFIG_FILE))
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        config_dict = dict()

    if choice == 1:
        config_dict['template'] = input('Path to the template: ')
    if choice == 2:
        config_dict['username'] = input('Username: ')
    if choice in (2, 3):
        try:
            username = config_dict['username']
        except KeyError:
            print(error_style('First enter your username.'))
            sys.exit()
        password = getpass.getpass('Password: ')
        keyring.set_password('codeforces-toolbox', username, password)
    if choice == 4:
        print('Set compile command, e.g. `g++ -Wall -O1`.\nIf you do not want to compile, just press enter.')
        config_dict['compile'] = input('Compile command: ')

    json.dump(config_dict, open(CONFIG_FILE, 'w'))
