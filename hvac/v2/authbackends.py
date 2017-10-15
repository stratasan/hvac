from .base import Feature


class AuthBackendsFeature(Feature):
    def list(self):
        return self.client.get('/v1/sys/auth').json()

    def mount(self, path, type=None, **kwargs):
        if not type:
            type = path
        params = {
            'type': type,
        }
        params.update(kwargs)

        self.client.post('/v1/sys/auth/{}'.format(path), json=params)

    def unmount(self, path):
        self.client.delete('/v1/sys/auth/{}'.format(path))

    def config(self, path):
        return self.client.get('/v1/sys/auth/{}/tune'.format(path)).json()

    def update_config(self, path, **kwargs):
        self.client.post('/v1/sys/auth/{}/tune'.format(path), json=kwargs)
