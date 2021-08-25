import sys
import time

import bs4
import keyring
import requests

from .constants import *


def submit(args):
    contest, problem_letter = translate_problem_name(args.problem)

    with requests.Session() as s:
        site = s.get('https://codeforces.com/enter')
        soup = bs4.BeautifulSoup(site.content, 'html.parser')
        csrf_token = soup.select_one('.csrf-token')['data-csrf']
        username = get_config('username')
        password = keyring.get_password('codeforces-toolbox', username)
        login_data = {'csrf_token': csrf_token, 'action': 'enter', 'handleOrEmail': username, 'password': password}
        login_response = s.post('https://codeforces.com/enter', data=login_data)
        login_response.raise_for_status()
        if bs4.BeautifulSoup(login_response.content, 'html.parser').select_one('span.error.for__password') is not None:
            print(error_style('Invalid username or password.'))
            sys.exit()

        site = s.get(f'https://codeforces.com/contest/{contest}/submit')
        soup = bs4.BeautifulSoup(site.content, 'html.parser')
        csrf_token = soup.select_one('.csrf-token')['data-csrf']
        language = get_config('language')
        with open(os.path.join(os.getcwd(), f'{contest}{problem_letter}.{language.ext}')) as f:
            solution = f.read()
        submit_data = {'csrf_token': csrf_token, 'submittedProblemIndex': problem_letter, 'programTypeId': language.n,
                       'source': solution}
        submit_response = s.post(f'https://codeforces.com/contest/{contest}/submit', data=submit_data)
        submit_response.raise_for_status()
        if bs4.BeautifulSoup(submit_response.content, 'html.parser').select_one('span.error.for__source') is not None:
            print(error_style('You have submitted exactly the same code before.'))
            sys.exit()

        print(info_style('Solution has been submitted.'))
        print('Verdict:')
        while True:
            site = s.get(f'https://codeforces.com/submissions/{username}')
            soup = bs4.BeautifulSoup(site.content, 'html.parser')
            v = soup.select_one('div.datatable table tr:nth-child(2) td.status-verdict-cell').text.strip()
            print('\033[F\033[K', end='')
            if v.startswith('Running') or v == 'In queue':
                print('Verdict: ' + info_style(v))
            elif v == 'Accepted':
                print('Verdict: ' + positive_style(v))
                break
            else:
                print('Verdict: ' + negative_style(v))
                break
            time.sleep(.05)
