class Feature:
    def __init__(self, client):
        self.client = client

class MountedFeature(Feature):
    def __init__(self, client, mount_path):
        super().__init__(client)
        self.mount_path = mount_path

    def auth(self, result):
        if result['wrap_info']:
            # TODO warn that response was wrapped but auth_token set?
            return

        self.client.token = result['auth']['client_token']
