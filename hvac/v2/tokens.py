from .base import Feature


class TokensFeature(Feature):
    def create(self, **kwargs):
        return self.client.post('/v1/auth/token/create', json=kwargs).json()

    def create_orphan(self, **kwargs):
        return self.client.post('/v1/auth/token/create-orphan', json=kwargs).json()

    def create_with_role(self, role_name, **kwargs):
        return self.client.post('/v1/auth/token/create/{}'.format(role_name), json=kwargs).json()

    def list(self):
        params = dict(list=True)
        return self.client.get('/v1/auth/token/accessors', params=params).json()

    def lookup(self, token):
        params = dict(token=token)
        return self.client.post('/v1/auth/token/lookup', json=params).json()

    def lookup_self(self):
        return self.client.get('/v1/auth/token/lookup-self').json()

    def lookup_accessor(self, accessor):
        params = dict(accessor=accessor)
        return self.client.post('/v1/auth/token/lookup-accessor', json=params).json()

    def renew(self, token, **kwargs):
        params = dict(token=token)
        params.update(kwargs)

        return self.client.post('/v1/auth/token/renew', json=params).json()

    def renew_self(self, **kwargs):
        return self.client.post('/v1/auth/token/renew-self', json=kwargs).json()

    def revoke(self, token):
        params = dict(token=token)
        self.client.post('/v1/auth/token/revoke', json=params)

    def revoke_self(self):
        self.client.post('/v1/auth/token/revoke-self')

    def revoke_accessor(self, accessor):
        params = dict(accessor=accessor)
        self.client.post('/v1/auth/token/revoke-accessor', json=params)

    def revoke_orphan(self, token):
        params = dict(token=token)
        self.client.post('/v1/auth/token/revoke-orphan', json=params)

    def role(self, name):
        return self.client.get('/v1/auth/token/roles/{}'.format(name)).json()

    def list_roles(self):
        params = dict(list=True)
        return self.client.get('/v1/auth/token/roles', params=params).json()

    def update_role(self, name, **kwargs):
        self.client.post('/v1/auth/token/roles/{}'.format(name), json=kwargs)

    def delete_role(self, name):
        self.client.delete('/v1/auth/token/roles/{}'.format(name))

    def tidy(self):
        self.client.post('/v1/auth/token/tidy')
