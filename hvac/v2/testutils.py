import subprocess
import time


class ServerManager(object):
    def __init__(self, config_path, client=None):
        self.config_path = config_path
        self.client = client

        self.process = None

        self.root_token = None
        self.keys = None

    def start(self, max_attempts=20, poll_interval=0.5):
        cmd = [
            'vault',
            'server', '-config=' + self.config_path
        ]

        self.process = subprocess.Popen(cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        attempts = 0
        last_exception = None
        while attempts < max_attempts:
            try:
                self.client.sys.health()
                return
            except Exception as ex:
                print('Waiting for Vault to start')

                time.sleep(poll_interval)

                attempts += 1
                last_exception = ex

        raise Exception('Unable to start Vault in background: {0}'.format(last_exception))

    def stop(self):
        self.process.kill()

    def initialize(self):
        result = self.client.sys.init()

        self.root_token = result['root_token']
        self.keys = result['keys']

        self.client.token = self.root_token

    def unseal(self):
        self.client.sys.unseal_multi(self.keys)
