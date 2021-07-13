import os
import sys
import requests
import bs4
import subprocess
from colorama import init as colorama_init
from termcolor import cprint


def add_subcommand_test(subparsers):
    parser = subparsers.add_parser('test', help='test the solution file')
    parser.add_argument('task', type=str, help='task id in the form "A" or "9999A"')
    parser.set_defaults(func=test)


def test(args):
    colorama_init()
    task = args.task
    if len(task) <= 2:
        task_letter = task
        contest = os.path.basename(os.getcwd())
    else:
        task_letter = task[4:]
        contest = task[:4]

    if os.path.exists(task_letter):
        os.chdir(task_letter)

    if not os.path.exists('in'):
        os.makedirs('in')
    if not os.path .exists('ans'):
        os.makedirs('ans')

    if len(os.listdir('in')) == 0:
        r = requests.get(f'https://codeforces.com/problemset/problem/{contest}/{task_letter}', )
        try:
            r.raise_for_status()
        except requests.HTTPError:
            cprint("Sorry, something went wrong while downloading tests", 'red', 'on_white')
            sys.exit()

        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        tests_input = soup.select('div.sample-test div.input pre')
        tests_answer = soup.select('div.sample-test div.output pre')
        for i, (test_in, test_ans) in enumerate(zip(tests_input, tests_answer), start=1):
            with open(f'in\\{i}.in', 'w') as input_file:
                input_file.write(test_in.string.lstrip())
            with open(f'ans\\{i}.out', 'w') as answer_file:
                answer_file.write(test_ans.string.lstrip())

    test_solution_file(contest + task_letter)


def test_solution_file(task):
    i = 1
    while os.path.exists(f'in\\{i}.in'):
        with open(f'in\\{i}.in') as input_file:
            test_in = input_file.read()
        with open(f'ans\\{i}.out') as answer_file:
            test_ans = answer_file.read()
        proc = subprocess.Popen([task], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            test_out, test_err = proc.communicate(input=bytes(test_in, 'utf-8'), timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            cprint('Execution time exceeded 5 seconds', 'red')
            sys.exit()

        test_out = test_out.decode('utf-8').lstrip()

        if test_out.split() == test_ans.split():    # delete every whitespace
            cprint('Test passed', 'green')
        else:
            cprint('Test did not pass', 'red')
            print('Program output:', test_out, sep='\n')
            print('Answer:', test_ans, sep='\n')

        i += 1
