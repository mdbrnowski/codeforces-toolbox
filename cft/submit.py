import os
import sys
import requests
import bs4
import json
import keyring
from termcolor import cprint
from .constants import CONFIG_FILE


def submit(args):
    problem = args.problem
    if len(problem) <= 2:
        problem_letter = problem
        contest = os.path.basename(os.getcwd())
        problem = contest + problem_letter
    else:
        problem_letter = problem[4:]
        contest = problem[:4]

    if os.path.exists(problem_letter):
        os.chdir(problem_letter)

    with requests.Session() as s:
        site = s.get('https://codeforces.com/enter')
        soup = bs4.BeautifulSoup(site.content, 'html.parser')
        csrf_token = soup.select_one('.csrf-token')['data-csrf']

        try:
            config_dict = json.load(open(CONFIG_FILE))
            username = config_dict['username']
        except FileNotFoundError:
            cprint('Configuration file not found', 'red', 'on_white')
            sys.exit()
        except KeyError:
            cprint('Specify your username first', 'red', 'on_white')

        password = keyring.get_password('codeforces-tool', username)
        login_data = {'csrf_token': csrf_token, 'action': 'enter', 'handleOrEmail': username, 'password': password}
        login_response = s.post('https://codeforces.com/enter', data=login_data)
        try:
            login_response.raise_for_status()
            if bs4.BeautifulSoup(login_response.content, 'html.parser').select_one('for__password') is not None:
                raise Exception('Invalid username or password')
        except requests.HTTPError:
            cprint("Sorry, something went wrong while logging in", 'red', 'on_white')
            sys.exit()
        except Exception as e:
            cprint(e, 'red', 'on_white')
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
            cprint("Sorry, something went wrong while submitting", 'red', 'on_white')
            sys.exit()
        cprint('Solution has been submitted', 'green')

        print('Verdict :')
        # TODO
