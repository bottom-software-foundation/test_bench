from __future__ import annotations
# import argparse

# def main():
#     parser = argparse.ArgumentParser(description='Runs a series of tests to measure the speed of libraries.')

#     parser.add_argument('-b', '--bottom', action='store_true', help='test the encoder')
#     parser.add_argument('-r', '--regress', action='store_true', help='test the decoder')

#     parser.add_argument('-c', '--command', help='the command that is executed to ')

import typer
import subprocess
import pathlib
import typing
import platform


def measure_command(cmd_args: typing.List[str]):
    system = platform.system()
    if system == 'Linux':
        args = ['perf', 'stat', '-r', '100', '-d']
        args.extend(cmd_args)
    elif system == 'Windows':
        args = ['powershell.exe', 'Measure-Command', '{']
        args.extend(cmd_args)
        args.extend(['|' 'powershell.exe', 'Out-Default', '}'])
    else:
        raise NotImplementedError("Unsupported Operating System.")

    return args


def execute_tests(command: str, tests: typing.Generator[pathlib.Path, None, None], param: str):
    for file in tests:
        desc, input_type, _ = file.name.split('.')

        to_execute = []

        if input_type == 'file':
            out_file = file.parent.parent / 'out' / (file.name + '.out')
            to_execute.extend([command, param, '-i', file.absolute(), '-o', out_file])
        
        to_execute = measure_command(to_execute)

        print('Running', file.name)

        o, e = subprocess.Popen(
            to_execute, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        print(file.name, 'Completed.')
        print(o.decode('utf-8').strip())
        if e:
            print('Errors:', e.decode('utf-8'))


def main(command: str = 'bottomify', bottom: bool = False, regress: bool = False):
    # o, e = subprocess.Popen(['time', 'echo', '"test"'])
    testsdir = pathlib.Path(__file__).resolve().parent.parent / 'tests'

    if bottom:
        bottom_tests = testsdir.glob('*.btm')

        execute_tests(command, bottom_tests, '-b')

    if regress:
        top_tests = testsdir.glob('*.top')
        execute_tests(command, top_tests, '--regress')


if __name__ == "__main__":
    typer.run(main)
