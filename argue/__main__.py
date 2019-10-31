from __future__ import print_function

import sys
import subprocess

import argparse


def compile_argv(command, optionals, positionals):
    new_argv = [command]

    for n, arg in sorted(optionals.items() + positionals.items()):
        new_argv.append(arg)

    return new_argv


def rekey_positionals(positionals, keys, new_keys):
    new_positionals = {}

    for key, new_key in zip(keys, new_keys):
            new_positionals[new_key] = positionals[key]

    return new_positionals


def prepend_positionals(positionals, prepend_text, prepend_keys):
    new_positionals = {}

    for key in positionals.keys():
        if key in prepend_keys:
            new_positionals[key] = prepend_text + positionals[key]
        else:
            new_positionals[key] = positionals[key]

    return new_positionals


def main(*args, **kwargs):
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--dry-run', action='store_true')

    modification_group = parser.add_argument_group(title='Modification')

    modification_group.add_argument('-s', '--skip-positionals', type=int)

    modification_group.add_argument('--prepend-after-operation', action='store_true')
    modification_group.add_argument('--prepend-all-positionals', type=str)
    modification_group.add_argument('--prepend-all-but-last-positional', type=str)
    modification_group.add_argument('--prepend-all-but-first-positional', type=str)

    #THIS IS THE FINAL PLAN
    #modification_group.add_argument('-l', '--lock-positionals', type=int, nargs='*')

    operation_group = parser.add_argument_group(title='Operation')
    operation_mutually_exclusive_group = operation_group.add_mutually_exclusive_group(required=True)

    operation_mutually_exclusive_group.add_argument('-r', '--positional-reversal', action='store_true')
    operation_mutually_exclusive_group.add_argument('-lf', '--positional-last-to-first', action='store_true')
    operation_mutually_exclusive_group.add_argument('-fl', '--positional-first-to-last', action='store_true')

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

    prepend_text = args.prepend_all_positionals \
        or args.prepend_all_but_first_positional \
        or args.prepend_all_but_last_positional

    prepend_keys = []

    if args.prepend_all_positionals:
        prepend_keys = sorted(positionals.keys())
    if args.prepend_all_but_first_positional:
        prepend_keys = sorted(positionals.keys())[1:]
    if args.prepend_all_but_last_positional:
        prepend_keys = sorted(positionals.keys())[:-1]

    argv = compile_argv(command, optionals, positionals)

    if prepend_keys and not args.prepend_after_operation:
        positionals = prepend_positionals(positionals, prepend_text, prepend_keys)

    if args.positional_reversal:
        keys = positionals.keys()
        keys_start =  keys[:args.skip_positionals]
        keys_end = sorted(keys[args.skip_positionals:])
        keys_end_reversed = keys[::-1]

        positionals = rekey_positionals(
            positionals,
            keys_start + keys_end,
            keys_start + keys_end_reversed
        )

    if args.positional_first_to_last:
        keys = positionals.keys()
        keys_start =  keys[:args.skip_positionals]
        keys_end = sorted(keys[args.skip_positionals:])
        keys_end_first_to_last = keys[:]

        positional = keys_end_first_to_last.pop()
        keys_end_first_to_last.insert(0, positional)

        positionals = rekey_positionals(
            positionals,
            keys_start + keys_end,
            keys_start + keys_end_first_to_last
        )

    if args.positional_last_to_first:
        keys = positionals.keys()
        keys_start =  keys[:args.skip_positionals]
        keys_end = sorted(keys[args.skip_positionals:])
        keys_end_last_to_first = keys[:]

        positional = keys_end_last_to_first.pop(0)
        keys_end_last_to_first.append(positional)

        positionals = rekey_positionals(
            positionals,
            keys_start + keys_end,
            keys_start + keys_end_last_to_first
        )

    if prepend_keys and args.prepend_after_operation:
        positionals = prepend_positionals(positionals, prepend_text, prepend_keys)

    new_argv = compile_argv(command, optionals, positionals)

    if args.dry_run:
        print('Arguments', args)
        print('Original Argv', argv)
        print('Modified Argv', new_argv)
    else:
        subprocess.call(new_argv)


if __name__ == '__main__':
    main()
