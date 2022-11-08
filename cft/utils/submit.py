import sys
import os
import time,datetime
import pickle

import bs4
import keyring
import requests

from .constants import *

SESSION_PATH=os.path.join(os.path.join(os.path.expanduser("~"), '.codeforces-toolbox'),"sessions")


def load_session(filename):
    dbfile = open(filename, 'rb')     
    db = pickle.load(dbfile)
    dbfile.close()
    return db



def dump_session(session,filename):
    if os.path.isfile(filename):
        os.remove(filename)
    dbfile = open(filename, 'ab')
    pickle.dump(session, dbfile)                     
    dbfile.close()
    return


def login():
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
        # removing session as it is expired
        if os.path.isfile(SESSION_PATH):
            os.remove(SESSION_PATH)
        dump_session(s,SESSION_PATH)


def check_time():
    if os.path.isfile(SESSION_PATH)==False:
        login()
    elif (datetime.datetime.now()-datetime.datetime(*time.gmtime(os.path.getmtime(SESSION_PATH))[:6])).days>1:
        print(negative_style("The login session have been expired and is login in again"))
        print(neutral_style("Login in again"))
        login()







def submit(args):
    contest, problem_letter = translate_problem_name(args.problem)
    check_time()
    with load_session(SESSION_PATH) as s:
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
        username = get_config('username')
        print(info_style('Solution has been submitted.'))
        print('Verdict:')
        while True:
            site = s.get(f'https://codeforces.com/submissions/{username}')
            soup = bs4.BeautifulSoup(site.content, 'html.parser')
            last_submission = soup.select_one('div.datatable table tr:nth-child(2)')
            verdict = last_submission.select_one('td.status-verdict-cell').text.strip()
            verdict_time = last_submission.select_one('td.time-consumed-cell').text.strip()
            verdict_memory = last_submission.select_one('td.memory-consumed-cell').text.strip()
            print('\033[F\033[K', end='')
            if verdict.startswith('Running') or verdict == 'In queue':
                print('Verdict: ' + info_style(verdict))
            else:
                print('Verdict:', end=' ')
                if verdict == 'Accepted':
                    print(positive_style(verdict))
                else:
                    print(negative_style(verdict))
                print('Time:    ' + verdict_time)
                print('Memory:  ' + verdict_memory)
                break
            time.sleep(.05)
