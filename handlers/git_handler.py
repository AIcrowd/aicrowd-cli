import os
import subprocess
import shlex

import click


class Git(object):
    def __init__(self, logger=None, ssh_private_key=None):
        self.logger = logger
        self.ssh = ssh_private_key

    def __getattr__(self, key):
        """Proxy the attribute request to function that executes subprocess."""
        return self._func_for_key(key)

    def call(self, key, args_string=None, **kwargs):
        return self._func_for_key(key)(args_string, **kwargs)

    def _log(self, message):
        if self.logger:
            self.logger.info(message)

    def _func_for_key(self, key):
        def proxy(cmd=None, **kwargs):
            args = ["git","lfs", key]
            if cmd:
                args.extend(shlex.split(cmd))
            self._log("Executing command: " + " ".join(args))
            git_env = os.environ.copy()
            if self.ssh:
                git_env['GIT_SSH_COMMAND'] = 'ssh -i %s' %(self.ssh)
            process = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=git_env
            )

            # output, error = process.communicate()
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                click.echo(line.decode('ascii'))
            output = process.stdout.readlines()
            return output, process.returncode
        return proxy
