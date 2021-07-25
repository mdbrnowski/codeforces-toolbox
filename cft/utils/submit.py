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
        username = get_username()
        password = keyring.get_password('codeforces-toolbox', username)
        login_data = {'csrf_token': csrf_token, 'action': 'enter', 'handleOrEmail': username, 'password': password}
        login_response = s.post('https://codeforces.com/enter', data=login_data)
        try:
            login_response.raise_for_status()
            if bs4.BeautifulSoup(login_response.content, 'html.parser').select_one('for__password') is not None:
                raise Exception('Invalid username or password.')
        except requests.HTTPError:
            print(error_style("Something went wrong while logging in."))
            sys.exit()
        except Exception as e:
            print(error_style(e))
            sys.exit()

        site = s.get(f'https://codeforces.com/contest/{contest}/submit')
        soup = bs4.BeautifulSoup(site.content, 'html.parser')
        csrf_token = soup.select_one('.csrf-token')['data-csrf']
        language = get_language()
        with open(os.path.join(os.getcwd(), f'{contest}{problem_letter}.{language.ext}')) as f:
            solution = f.read()
        submit_data = {'csrf_token': csrf_token, 'submittedProblemIndex': problem_letter, 'programTypeId': language.n,
                       'source': solution}
        submit_response = s.post(f'https://codeforces.com/contest/{contest}/submit', data=submit_data)
        try:
            submit_response.raise_for_status()
        except requests.HTTPError:
            print(error_style("Something went wrong while submitting."))
            sys.exit()
        print('Solution has been submitted.')

        print('Verdict:', end=' ')
        while True:
            site = s.get(f'https://codeforces.com/submissions/{username}')
            soup = bs4.BeautifulSoup(site.content, 'html.parser')
            v = soup.select_one('div.datatable table tr:nth-child(2) td.status-verdict-cell').text.strip()
            if not (v.startswith('Running') or v == 'In queue'):
                if v == 'Accepted':
                    print(positive_style(v))
                else:
                    print(negative_style(v))
                break
            time.sleep(2)
