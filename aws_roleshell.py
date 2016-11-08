import argparse
import os
try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

from awscli.customizations.commands import BasicCommand


def awscli_initialize(event_hooks):
    event_hooks.register('building-command-table.main', inject_commands)


def inject_commands(command_table, session, **kwargs):
    command_table['roleshell'] = RoleShell(session)


def print_creds(environment_overrides):
    exports = []
    for var, value in environment_overrides.items():
        if value is not None:
            exports.append("export {}={}".format(var, cmd_quote(value)))
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
    os.execvp(command[0], command)


def run_shell(environment_overrides, command):
    # If the first argument to the shell begins with -, the user will want to
    # separate the remainder of the arguments list with --, which awscli will
    # unhelpfully pass on to us.
    command.insert(0, os.environ['SHELL'])
    run_command(environment_overrides, command)


class RoleShell(BasicCommand):
    NAME = 'roleshell'
    DESCRIPTION = (
        'Executes a command with temporary AWS credentials provided as '
        'environment variables')
    ARG_TABLE = [
        dict(name='shell', action='store_true', help_text='Execute the current '
             'shell instead of a command.  Any remaining arguments, if any, '
             'are passed on to the new shell.'),
        dict(name='command', nargs=argparse.REMAINDER, positional_arg=True,
             synopsis='[command] [args ...]'),
    ]

    def _build_environment_overrides(self):
        environment_overrides = {}

        creds = self._session.get_credentials()
        environment_overrides['AWS_ACCESS_KEY_ID'] = creds.access_key
        environment_overrides['AWS_SECRET_ACCESS_KEY'] = creds.secret_key
        environment_overrides['AWS_SESSION_TOKEN'] = creds.token

        region = self._session.get_config_variable('region')
        environment_overrides['AWS_DEFAULT_REGION'] = region

        return environment_overrides

    def _run_main(self, args, parsed_globals):
        environment_overrides = self._build_environment_overrides()

        if args.command[0:1] == ["--"]:
            args.command.pop(0)

        if args.shell:
            run_shell(environment_overrides, args.command)
        elif args.command:
            run_command(environment_overrides, args.command)
        else:
            print_creds(environment_overrides)
