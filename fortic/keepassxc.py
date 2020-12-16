import logging
import os
from pathlib import Path

from .keepassxc_browser import Connection, Identity, ProtocolError


class KeePassXCClient:

    def __init__(self):

        client_id = 'python-keepassxc-browser'

        self.state_file = Path(os.path.expanduser(os.path.join("~", ".python_keepassxc_browser")))

        if self.state_file.exists():
            with self.state_file.open('r') as f:
                data = f.read()
            self.id = Identity.unserialize(client_id, data)
        else:
            self.id = Identity(client_id)

        self.keepassxc = Connection()

    def connect(self):
        self.keepassxc.connect()
        self.keepassxc.change_public_keys(self.id)
        try:
            db_hash = self.keepassxc.get_database_hash(self.id)
        except ProtocolError as ex:
            print(ex)
            exit(1)

        if not self.keepassxc.test_associate(self.id):
            logging.info('Not associated yet, associating now...')
            assert self.keepassxc.associate(self.id)
            data = self.id.serialize()
            with self.state_file.open('w') as f:
                f.write(data)
            del data

    def get_logins(self, url):
        self.connect()
        login = self.keepassxc.get_logins(self.id, url=url)
        self.disconnect()
        return login

    def disconnect(self):
        self.keepassxc.disconnect()
