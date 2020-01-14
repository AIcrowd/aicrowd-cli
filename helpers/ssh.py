import logging
import os

import click
import ssh_agent_setup
from Crypto.PublicKey import RSA

class SSHHandler():
    def __init__(self, private_key_file, public_key_file):
        self.private_file = private_key_file
        self.public_file = public_key_file

    def generate_keys(self):
        os.makedirs(os.path.dirname(self.private_file), exist_ok=True)
        key = RSA.generate(2048)
        click.echo(self.private_file)
        click.echo(self.public_file)
        private_file = open(self.private_file, "wb")
        private_file.write(key.exportKey('PEM'))
        private_file.close()
        pubkey = key.publickey()
        public_file = open(self.public_file, "wb")
        public_file.write(pubkey.exportKey('OpenSSH'))
        public_file.close()
        logging.info("add this ssh key at: https://gitlab.aicrowd.com/profile/keys")
        logging.info(pubkey.exportKey('OpenSSH'))
        return pubkey.exportKey('OpenSSH')

    def sshagent(self):
        ssh_agent_setup.setup()
        try:
            ssh_agent_setup.addKey(self.private_file)
        except Exception as e:
            logging.debug(e)
            logging.info("Please generate ssh keys")
