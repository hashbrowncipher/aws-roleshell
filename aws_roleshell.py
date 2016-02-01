import argparse
import os
import shlex
import textwrap

from awscli.customizations.commands import BasicCommand


def awscli_initialize(event_hooks):
    event_hooks.register('building-command-table.main', inject_commands)


def inject_commands(command_table, session, **kwargs):
    command_table['roleshell'] = RoleShell(session)


def print_creds(creds):
    quoted_vars = map(shlex.quote, (creds.access_key,
                                    creds.secret_key, creds.token))

    print(textwrap.dedent("""\
        export AWS_ACCESS_KEY_ID={}
        export AWS_SECRET_ACCESS_KEY={}
        export AWS_SESSION_TOKEN={}\
    """.format(*quoted_vars)))


def get_exec_args(input_command):
    if len(input_command) == 0:
        input_command = (os.environ['SHELL'],)

    return (input_command[0], input_command)


def run_command(creds, command):
    os.environ['AWS_ACCESS_KEY_ID'] = creds.access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = creds.secret_key
    os.environ['AWS_SESSION_TOKEN'] = creds.token

    os.execvp(*get_exec_args(command))


class RoleShell(BasicCommand):
    NAME = 'roleshell'
    DESCRIPTION = (
        'Executes a shell with temporary AWS credentials provided as environment variables')
    ARG_TABLE = [
        dict(name='command', nargs=argparse.REMAINDER, positional_arg=True),
    ]

    def _run_main(self, args, parsed_globals):
        c = self._session.get_credentials()

        if len(args.command) == 0:
            print_creds(c)
        else:
            run_command(c, args.command)
