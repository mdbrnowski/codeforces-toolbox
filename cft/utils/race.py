import shutil

import bs4
import requests

from .constants import *


def race(args):
    language = get_config('language')
    contest = args.contest
    template = get_config('template')
    if not os.path.exists(template):
        print(error_style('Template file does not exist.'))
        sys.exit()
    try:
        os.makedirs(contest)
    except OSError:
        print(error_style(f'Folder {contest} already exists.'))
        sys.exit()
    os.chdir(contest)
    for problem_letter in contest_letters(contest):
        shutil.copy(template, f'{contest}{problem_letter}.{language.ext}')


def contest_letters(contest):
    r = requests.get(f'https://codeforces.com/contest/{contest}')
    try:
        r.raise_for_status()
        if len(r.history):
            raise requests.HTTPError
    except requests.HTTPError:
        print(warning_style('Something went wrong while accessing problems'))
        return contest_letters_default(contest)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    letters = soup.select('table.problems tr:nth-child(n+2) td:first-child a')
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
