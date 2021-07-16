import os
import shutil
import sys
import requests
import bs4
import json
from termcolor import cprint
from .constants import CONFIG_FILE

try:
    config_dict = json.load(open(CONFIG_FILE))
    template = config_dict['template']
except (FileNotFoundError, KeyError):
    template = ''


def race(args):
    contest = args.contest
    if not os.path.exists(template):
        cprint('Template does not exist', 'red', 'on_white')
        sys.exit()
    os.makedirs(contest)
    os.chdir(contest)
    for problem_letter in contest_letters(contest):
        shutil.copy(template, f'{contest}{problem_letter}.cpp')


def contest_letters(contest):
    r = requests.get(f'https://codeforces.com/contest/{contest}')
    try:
        r.raise_for_status()
    except requests.HTTPError:
        cprint('Invalid contest', 'red', 'on_white')
        return contest_letters_default(contest)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    letters = soup.select('table.problems tr:nth-child(n+2) td:first-child a')
    if not letters:
        cprint('Something went wrong while accessing problems', 'red', 'on_white')
        return contest_letters_default(contest)
    return [letter.text.strip() for letter in letters]


def contest_letters_default(contest):
    d = input('Do you want to create default A-G files? [y/n] ')
    if d.lower() in ('y', 'yes'):
        return list('ABCDEFG')
    else:
        print('Aborted')
        os.chdir('..')
        os.rmdir(contest)
        sys.exit()
