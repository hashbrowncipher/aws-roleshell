import argparse
import os
import shlex

from awscli.customizations.commands import BasicCommand


def awscli_initialize(event_hooks):
    event_hooks.register('building-command-table.main', inject_commands)


def inject_commands(command_table, session, **kwargs):
    command_table['roleshell'] = RoleShell(session)


def print_creds(environment_overrides):
    exports = []
    for var, value in environment_overrides.items():
        if value is not None:
            exports.append("export {}={}".format(var, shlex.quote(value)))
        else:
            exports.append("unset {}".format(var))

    print("\n".join(exports))


def get_exec_args(input_command):
    if len(input_command) == 0:
        input_command = (os.environ['SHELL'],)

    return (input_command[0], input_command)


def run_command(environment_overrides, command):
    for var, value in environment_overrides.items():
        if value is not None:
            os.environ[var] = environment_overrides[var]
        elif var in os.environ:
            del os.environ[var]

    # TODO: use a copy of the environment with variables deleted, to support
    # platforms without unsetenv() support.
    os.execvp(*get_exec_args(command))


class RoleShell(BasicCommand):
    NAME = 'roleshell'
    DESCRIPTION = (
        'Executes a shell with temporary AWS credentials provided as '
        'environment variables')
    ARG_TABLE = [
        dict(name='command', nargs=argparse.REMAINDER, positional_arg=True),
    ]

    def _build_environment_overrides(self):
        environment_overrides = {}

        creds = self._session.get_credentials()
        environment_overrides['AWS_ACCESS_KEY_ID'] = creds.access_key
        environment_overrides['AWS_SECRET_ACCESS_KEY'] = creds.secret_key
        environment_overrides['AWS_SESSION_TOKEN'] = creds.token

        return environment_overrides

    def _run_main(self, args, parsed_globals):
        environment_overrides = self._build_environment_overrides()

        if len(args.command) == 0:
            print_creds(environment_overrides)
        else:
            run_command(environment_overrides, args.command)
