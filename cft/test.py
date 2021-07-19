import json
import subprocess

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
                answer_file.write(test_ans.string.strip())

    if compile_solution(problem).returncode != 0:
        print_error('Solution has not been compiled.')
        sys.exit()
    else:
        print('Solution has been compiled.')

    i = 1
    while os.path.exists(f'in\\{i}.in'):
        test_solution_file(problem, i)
        i += 1


def compile_solution(problem):
    try:
        config_dict = json.load(open(CONFIG_FILE))
        compile_command = config_dict['compile']
    except FileNotFoundError:
        print_error('Configuration file has not been found.')
        sys.exit()
    except KeyError:
        print_error('Specify compile command first.')
        sys.exit()

    try:
        return subprocess.run(f'{compile_command} {problem}.cpp -o {problem}')
    except OSError:
        print_error('Compile command is wrong or compiler is not installed.')
        sys.exit()


def test_solution_file(solution, i):
    with open(f'in\\{i}.in') as input_file:
        test_in = input_file.read()
    with open(f'ans\\{i}.out') as answer_file:
        test_ans = answer_file.read()

    try:
        r = subprocess.run(solution, input=test_in, capture_output=True, timeout=5, encoding='utf-8')
        test_out = r.stdout.strip()
        test_err = r.stderr.strip()
    except subprocess.TimeoutExpired:
        print_bad('Execution time exceeded 5 seconds')
        return

    if test_out.split() == test_ans.split():    # delete every whitespace
        print_good('Test passed')
    else:
        print_bad('Test did not pass')
        print('Program output:', test_out, sep='\n')
        if test_err:
            print('\nProgram error:', test_err, sep='\n')
        print('\nAnswer:', test_ans, sep='\n')

