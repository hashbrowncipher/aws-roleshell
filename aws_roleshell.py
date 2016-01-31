from awscli.customizations.commands import BasicCommand

import os

def awscli_initialize(event_hooks):
    event_hooks.register('building-command-table.main', inject_commands)

def inject_commands(command_table, session, **kwargs):
    command_table['roleshell'] = RoleShell(session)

class RoleShell(BasicCommand):
    NAME = 'roleshell'
    DESCRIPTION = ('Executes a shell with temporary AWS credentials provided as environment variables')

    def _run_main(self, args, parsed_globals):
        a = self._session.get_credentials()
        os.environ['AWS_ACCESS_KEY_ID'] = a.access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = a.secret_key
        os.environ['AWS_SESSION_TOKEN'] = a.token

        shell = os.environ['SHELL']
        os.execv(shell, [shell])
