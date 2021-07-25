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
            os.remove(os.path.join('in', file))
        for file in os.listdir('ans'):
            os.remove(os.path.join('ans', file))

    if len(os.listdir('in')) == 0:
        r = requests.get(f'https://codeforces.com/problemset/problem/{contest}/{problem_letter}')
        try:
            r.raise_for_status()
        except requests.HTTPError:
            print(error_style("Something went wrong while downloading tests"))
            sys.exit()

        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        tests_input = soup.select('div.sample-test div.input pre')
        tests_answer = soup.select('div.sample-test div.output pre')
        for i, (test_in, test_ans) in enumerate(zip(tests_input, tests_answer), start=1):
            with open(os.path.join('in', f'{i}.in'), 'w') as input_file:
                input_file.write(test_in.string.lstrip())
            with open(os.path.join('ans', f'{i}.out'), 'w') as answer_file:
                answer_file.write(test_ans.string.strip())

    compile_command = get_compile_command()
    if compile_command:
        if compile_solution(problem, compile_command).returncode != 0:
            print(error_style('Solution has not been compiled.'))
            sys.exit()
        else:
            print('Solution has been compiled.')

    i = 1
    while os.path.exists(os.path.join('in', f'{i}.in')):
        test_solution(problem, i)
        i += 1


def compile_solution(problem, compile_command):
    language = get_language()
    try:
        return subprocess.run([*compile_command.split(' '), f'{problem}.{language.ext}', '-o', problem])
    except OSError:
        print(error_style('Compile command is wrong or compiler is not installed.'))
        sys.exit()


def test_solution(problem, i):
    with open(os.path.join('in', f'{i}.in')) as input_file:
        test_in = input_file.read()
    with open(os.path.join('ans', f'{i}.out')) as answer_file:
        test_ans = answer_file.read()

    language = get_language()
    run_command = get_run_command()
    try:
        if run_command:
            r = subprocess.run([*run_command.split(' '), f'{problem}.{language.ext}'], input=test_in,
                               capture_output=True, timeout=10, encoding='utf-8')
        else:
            r = subprocess.run('./' + problem, input=test_in, capture_output=True, timeout=10, encoding='utf-8')
        test_out = r.stdout.strip()
        test_err = r.stderr.strip()
    except FileNotFoundError:
        print(error_style('Executable file has not been found.'))
        print('If your are using a compiled language (' + neutral_style('C++') + ', ' + neutral_style('C') +
              '), set compile command.')
        print('If you are using a interpreted language (' + neutral_style('Python') + '), set run command.')
        sys.exit()
    except subprocess.TimeoutExpired:
        print(negative_style('Execution time exceeded 10 seconds'))
        return

    if test_out.split() == test_ans.split():    # delete every whitespace
        print(positive_style('Test passed'))
    else:
        print(negative_style('Test did not pass'))
        print('Program output:', test_out, sep='\n')
        if test_err:
            print('\nProgram error:', test_err, sep='\n')
        print('\nAnswer:', test_ans, sep='\n')
