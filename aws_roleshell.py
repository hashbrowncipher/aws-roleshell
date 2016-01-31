import argparse

from awscli.customizations.commands import BasicCommand

import os

def awscli_initialize(event_hooks):
    event_hooks.register('building-command-table.main', inject_commands)

def inject_commands(command_table, session, **kwargs):
    command_table['roleshell'] = RoleShell(session)

def get_exec_args(input_command):
    if len(input_command) == 0:
        input_command = (os.environ['SHELL'],)

    return (input_command[0], input_command)


class RoleShell(BasicCommand):
    NAME = 'roleshell'
    DESCRIPTION = ('Executes a shell with temporary AWS credentials provided as environment variables')
    ARG_TABLE = [
        dict(name='command', nargs=argparse.REMAINDER, positional_arg=True),
    ]

    def _run_main(self, args, parsed_globals):
        a = self._session.get_credentials()
        os.environ['AWS_ACCESS_KEY_ID'] = a.access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = a.secret_key
        os.environ['AWS_SESSION_TOKEN'] = a.token

        os.execvp(*get_exec_args(args.command))
