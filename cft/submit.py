import json
import os
import sys

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

        try:
            config_dict = json.load(open(CONFIG_FILE))
            username = config_dict['username']
        except FileNotFoundError:
            print_error('Configuration file has not been found.')
            sys.exit()
        except KeyError:
            print_error('Specify your username first.')
            sys.exit()

        password = keyring.get_password('codeforces-tool', username)
        login_data = {'csrf_token': csrf_token, 'action': 'enter', 'handleOrEmail': username, 'password': password}
        login_response = s.post('https://codeforces.com/enter', data=login_data)
        try:
            login_response.raise_for_status()
            if bs4.BeautifulSoup(login_response.content, 'html.parser').select_one('for__password') is not None:
                raise Exception('Invalid username or password')
        except requests.HTTPError:
            print_error("Something went wrong while logging in.")
            sys.exit()
        except Exception as e:
            print_error(e)
            sys.exit()

        site = s.get(f'https://codeforces.com/contest/{contest}/submit')
        soup = bs4.BeautifulSoup(site.content, 'html.parser')
        csrf_token = soup.select_one('.csrf-token')['data-csrf']
        with open(os.path.join(os.getcwd(), f'{contest}{problem_letter}.cpp')) as f:
            solution = f.read()
        submit_data = {'csrf_token': csrf_token, 'submittedProblemIndex': problem_letter, 'programTypeId': '54',
                       'source': solution}
        submit_response = s.post(f'https://codeforces.com/contest/{contest}/submit', data=submit_data)
        try:
            submit_response.raise_for_status()
        except requests.HTTPError:
            print_error("Something went wrong while submitting")
            sys.exit()
        print('Solution has been submitted')

        print('Verdict :')
        # TODO
