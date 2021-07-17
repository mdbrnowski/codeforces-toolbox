import os
import subprocess
import sys

import bs4
import requests

from .constants import *


def test(args):
    contest, problem_letter = translate_problem_name(args.problem)
    problem = contest + problem_letter

    if not os.path.exists('in'):
        os.makedirs('in')
    if not os.path.exists('ans'):
        os.makedirs('ans')

    if args.download:
        for file in os.listdir('in'):
            os.remove(f'in\\{file}')
        for file in os.listdir('ans'):
            os.remove(f'ans\\{file}')

    if len(os.listdir('in')) == 0:
        r = requests.get(f'https://codeforces.com/problemset/problem/{contest}/{problem_letter}')
        try:
            r.raise_for_status()
        except requests.HTTPError:
            print_error("Something went wrong while downloading tests")
            sys.exit()

        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        tests_input = soup.select('div.sample-test div.input pre')
        tests_answer = soup.select('div.sample-test div.output pre')
        for i, (test_in, test_ans) in enumerate(zip(tests_input, tests_answer), start=1):
            with open(f'in\\{i}.in', 'w') as input_file:
                input_file.write(test_in.string.lstrip())
            with open(f'ans\\{i}.out', 'w') as answer_file:
                answer_file.write(test_ans.string.lstrip())

    if not os.access(f'{problem}.exe', os.F_OK | os.X_OK) or os.access(f'{problem}', os.F_OK | os.X_OK):
        print_error('Solution is not compiled')
        sys.exit()

    i = 1
    while os.path.exists(f'in\\{i}.in'):
        test_solution_file(problem, i)
        i += 1


def test_solution_file(solution, i):
    with open(f'in\\{i}.in') as input_file:
        test_in = input_file.read()
    with open(f'ans\\{i}.out') as answer_file:
        test_ans = answer_file.read()
    proc = subprocess.Popen([solution], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        test_out, test_err = proc.communicate(input=bytes(test_in, 'utf-8'), timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        print_bad('Execution time exceeded 5 seconds')
        return

    test_out = test_out.decode('utf-8').lstrip()

    if test_out.split() == test_ans.split():    # delete every whitespace
        print_good('Test passed')
    else:
        print_bad('Test did not pass')
        print('Program output:', test_out, sep='\n')
        print('Answer:', test_ans, sep='\n')
