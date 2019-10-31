from __future__ import print_function

import sys
import subprocess

import argparse


def main(*args, **kwargs):
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--dry-run', action='store_true')

    operation_group = parser.add_mutually_exclusive_group(required=True)

    operation_group.add_argument('-r', '--positional-reversal', action='store_true')
    operation_group.add_argument('-lf', '--positional-last-to-first', action='store_true')
    operation_group.add_argument('-fl', '--positional-first-to-last', action='store_true')

    parser.add_argument('argv', nargs='+')

    args = parser.parse_args()

    command = args.argv.pop(0)

    optionals = {}
    positionals = {}

    for n, arg in enumerate(args.argv):
        if arg.startswith('-'):
            optionals[n] = arg
        else:
            positionals[n] = arg

    nargs = n

    if args.positional_reversal:
        positional_keys = sorted(positionals.keys())
        positional_keys_reversed = positional_keys[::-1]

        new_positionals = {}

        for key, new_key in zip(positional_keys, positional_keys_reversed):
            new_positionals[new_key] = positionals[key]

        positionals = new_positionals

    if args.positional_last_to_first:
        positional_keys = sorted(positionals.keys())
        positional_keys_last_to_first = positional_keys[:]

        positional = positional_keys_last_to_first.pop(0)
        positional_keys_last_to_first.append(positional)

        new_positionals = {}

        for key, new_key in zip(positional_keys, positional_keys_last_to_first):
            new_positionals[new_key] = positionals[key]

        positionals = new_positionals

    if args.positional_first_to_last:
        positional_keys = sorted(positionals.keys())
        positional_keys_first_to_last = positional_keys[:]

        positional = positional_keys_first_to_last.pop()
        positional_keys_first_to_last.insert(0, positional)

        new_positionals = {}

        for key, new_key in zip(positional_keys, positional_keys_first_to_last):
            new_positionals[new_key] = positionals[key]

        positionals = new_positionals

    optionals_and_positionals = {}

    optionals_and_positionals.update(optionals)
    optionals_and_positionals.update(positionals)

    new_argv = [command]

    for n, arg in sorted(optionals_and_positionals.items()):
        new_argv.append(arg)

    if args.dry_run:
        print(new_argv)
    else:
        subprocess.call(new_argv)

if __name__ == '__main__':
    main()
