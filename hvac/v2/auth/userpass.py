from ..base import MountedFeature


class UserPassFeature(MountedFeature):
    def login(self, username, password, use_token=True):
        params = dict(password=password)
        path = '/v1/auth/{}/login/{}'.format(self.mount_path, username)

        result = self.client.post(path, json=params).json()
        if use_token:
            self.auth(result)

        return result

    def list_users(self):
        params = dict(list=True)
        path = '/v1/auth/{}/users'.format(self.mount_path)
        return self.client.get(path, params=params).json()

    def update_user(self, username, password, **kwargs):
        params = dict(password=password)
        params.update(kwargs)

        path = '/v1/auth/{}/users/{}'.format(self.mount_path, username)
        self.client.post(path, json=params)

    def user(self, username):
        path = '/v1/auth/{}/users/{}'.format(self.mount_path, username)
        return self.client.get(path).json()

    def delete_user(self, username):
        path = '/v1/auth/{}/users/{}'.format(self.mount_path, username)
        self.client.delete(path)
