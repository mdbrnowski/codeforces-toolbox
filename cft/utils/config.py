import getpass

import keyring

from .constants import *


def config(args):
    print('Choose one of the following (type an integer):',
          '  1. change the template file',
          '  2. change username and password',
          '  3. change password',
          '  4. change language',
          '  5. set compile command',
          sep='\n')
    try:
        while (choice := input()) not in {'1', '2', '3', '4', '5'}:
            print(warning_style('Type an integer 1-5:'))
        choice = int(choice)
    except KeyboardInterrupt:
        print(warning_style('Aborted.'))
        sys.exit(0)

    if not os.path.exists(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox')):
        os.makedirs(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox'))

    try:
        config_dict = json.load(open(CONFIG_FILE))
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        config_dict = dict()

    try:
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
            print('Change your programming language and the program that Codeforces will use to run your solution.')
            print('Choose one of the following (type an integer):')
            for key, lan in LANGUAGES.items():
                print(f'    {key}. {lan.name:30}' + neutral_style(lan.ext))
            try:
                while (language := input()) not in LANGUAGES.keys():
                    print(warning_style('Type an integer 1-5:'))
            except KeyboardInterrupt:
                print(warning_style('Aborted.'))
                sys.exit(0)
            config_dict['language'] = (LANGUAGES[language].n, LANGUAGES[language].name, LANGUAGES[language].ext)

        if choice == 5:
            print('Set compile command, e.g. `g++ -Wall -O1`.\nIf you do not want to compile, just press enter.')
            config_dict['compile'] = input('Compile command: ')
    finally:
        json.dump(config_dict, open(CONFIG_FILE, 'w'))
