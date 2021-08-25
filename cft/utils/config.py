import getpass

import keyring

from .constants import *
from .upgrade import try_upgrade


def config(args):
    try_upgrade()

    print('Choose one of the following (type an integer):')
    options = [('1. change the template file', get_config('template', strict=False)),
               ('2. change username and password', get_config('username', strict=False)),
               ('3. change programming language', get_config('language', strict=False).name),
               ('4. set compile command', get_config('compile', strict=False)),
               ('5. set run command', get_config('run', strict=False))]
    for option, current in options:
        if current and option.startswith('1') and not os.path.exists(current):
            current = '  ' + info_style('[') + error_style(current) + info_style(']')
        elif current:
            current = '  ' + info_style('[') + neutral_style(current) + info_style(']')
        print(f'  {option}{current}')

    print('Option: ', end='')
    while (choice := input()) not in list('12345'):
        print(warning_style('Type an integer 1-5: '), end='')
    choice = int(choice)

    if choice == 1:
        set_config('template', input('Path to the template: '))

    if choice == 2:
        username = set_config('username', input('Username: '))
        password = getpass.getpass('Password: ')
        keyring.set_password('codeforces-toolbox', username, password)

    if choice == 3:
        print('Change your programming language and the program that Codeforces will use to run your solution.')
        print('Choose one of the following (type an integer):')
        for key, lan in LANGUAGES.items():
            print(f'    {key + "." :3} {lan.name:30}' + neutral_style(lan.ext))
        print('Option: ', end='')
        while (language := input()) not in LANGUAGES.keys():
            print(warning_style('Type an integer 1-18: '), end='')
        set_config('language', (LANGUAGES[language].n, LANGUAGES[language].name, LANGUAGES[language].ext))

    if choice == 4:
        print('Set compile command, e.g. `g++ -Wall -O1`.')
        print('If you are using ' + neutral_style('Python') +
              ' or do not want to compile your solutions, just press enter.')
        set_config('compile', input('Compile command: '))

    if choice == 5:
        print('Set run command, e.g. `python` or enter an absolute path to the interpreter.')
        print('If you are using any language other than ' + neutral_style('Python') + ' or ' + neutral_style('Java')
              + ', you can just press enter, your run command will be just `./`.')
        set_config('run', input('Run command: '))
