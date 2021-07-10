import os


def add_subcommand_test(subparsers):
    parser = subparsers.add_parser('test', help='test the solution file')
    parser.add_argument('task', type=str, help='task id in the form "A" or "9999A"')
    parser.set_defaults(func=test)


def test(args):
    task = args.task
    if len(task) <= 2:
        task_letter = task
        task = os.path.basename(os.getcwd()) + task
    else:
        task_letter = task[4:]

    if os.path.exists(task_letter):
        os.chdir(task_letter)

    if not os.path.exists('in'):
        os.makedirs('in'), os.makedirs('out')
        # TODO: download tests from statement

    # TODO: execute tests and compare output
