from __future__ import annotations

import pathlib
import platform
import shlex
import subprocess
import typing

import typer
from rich import print


def measure_command(cmd_args: typing.List[typing.List[str]]):
    base = ['hyperfine', '--show-output', '--min-runs', '5']

    for test_cmd in cmd_args:
        print(shlex.quote(shlex.join(test_cmd)))
        base.append(shlex.quote(shlex.join(test_cmd)))

    return base


def execute_tests(command: str, tests: typing.Generator[pathlib.Path, None, None], param: str):
    tests = list(tests)

    if tests:
        print(f'[yellow]found {len(tests)} test(s).[/yellow]')
    else:
        print(f'[red]no tests found.[/red]')
        return

    to_execute = []

    for file in tests:
        desc, input_type, _ = file.name.split('.')

        if input_type == 'file':
            out_file = file.parent.parent / 'out' / (file.name + '.out')
            to_execute.append([shlex.quote(command), param, '-i', str(file.absolute()), '-o', str(out_file.absolute())])

        print(f'[green]Loaded {desc} ({input_type}) [/green]')
        
    if to_execute:
        subprocess.Popen(measure_command(to_execute)).communicate()


def main(command: str, bottom: bool = False, regress: bool = False):
    testsdir = pathlib.Path(__file__).resolve().parent.parent / 'tests'

    if bottom:
        print('[blue]running bottom tests...[/blue]')
        bottom_tests = testsdir.glob('*.btm')
        execute_tests(command, bottom_tests, '--bottomify')
        print('[green]bottom tests complete.[/green]')

    if regress:
        print('[blue]running regress tests...[/blue]')
        top_tests = testsdir.glob('*.top')
        execute_tests(command, top_tests, '--regress')
        print('[green]regress tests complete.[/green]')


if __name__ == "__main__":
    typer.run(main)
