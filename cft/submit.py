def add_subcommand_submit(subparsers):
    parser = subparsers.add_parser('submit')
    parser.add_argument('task', type=str, help='number of the task in the form "A" or "9999A"')
    parser.set_defaults(func=submit)


def submit(args):
    print('Submitting task', args.task)
    # TODO
