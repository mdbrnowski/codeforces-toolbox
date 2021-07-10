def add_subcommand_submit(subparsers):
    parser = subparsers.add_parser('submit', help='submit solution')
    parser.add_argument('task', type=str, help='task id in the form "A" or "9999A"')
    parser.set_defaults(func=submit)


def submit(args):
    print('Submitting task', args.task)
    # TODO
