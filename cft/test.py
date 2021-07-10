def add_subcommand_test(subparsers):
    parser = subparsers.add_parser('test', help='test the solution file')
    parser.add_argument('task', type=str, help='task id in the form "A" or "9999A"')
    parser.set_defaults(func=test)


def test(args):
    print('Testing task', args.task)
    # TODO
