from ..base import MountedFeature


class AppRoleFeature(MountedFeature):
    def login(self, role_id, secret_id=None, use_token=True, **kwargs):
        params = {
            'role_id': role_id,
        }
        if secret_id:
            params['secret_id'] = secret_id

        params.update(kwargs)

        result = self.client.post('/v1/auth/{}/login'.format(self.mount_path), json=params).json()
        if use_token:
            self.auth(result)

        return result

    def list_roles(self):
        params = dict(list=True)
        return self.client.get('/v1/auth/{}/role'.format(self.mount_path), params=params).json()

    def update_role(self, name, **kwargs):
        self.client.post('/v1/auth/{}/role/{}'.format(self.mount_path, name), json=kwargs)

    def role(self, name):
        return self.client.get('/v1/auth/{}/role/{}'.format(self.mount_path, name)).json()

    def delete_role(self, name):
        self.client.delete('/v1/auth/{}/role/{}'.format(self.mount_path, name))

    def role_id(self, name):
        path = '/v1/auth/{}/role/{}/role-id'.format(self.mount_path, name)
        return self.client.get(path).json()

    def update_role_id(self, name, role_id):
        params = dict(role_id=role_id)
        path = '/v1/auth/{}/role/{}/role-id'.format(self.mount_path, name)
        self.client.post(path, json=params)

    def create_secret_id(self, name, **kwargs):
        path = '/v1/auth/{}/role/{}/secret-id'.format(self.mount_path, name)
        return self.client.post(path, json=kwargs).json()

    def list_secret_id_accessors(self, name, **kwargs):
        params = dict(list=True)
        path = '/v1/auth/{}/role/{}/secret-id'.format(self.mount_path, name)
        return self.client.get(path, params=params).json()

    def lookup_secret_id(self, name, secret_id_accessor):
        params = dict(secret_id_accessor=secret_id_accessor)
        path = '/v1/auth/{}/role/{}/secret-id-accessor/lookup'.format(self.mount_path, name)
        return self.client.get(path, params=params).json()

    def destroy_secret_id(self, name, secret_id_accessor):
        params = dict(secret_id_accessor=secret_id_accessor)
        path = '/v1/auth/{}/role/{}/secret-id-accessor/destroy'.format(self.mount_path, name)
        self.client.post(path, params=params)
