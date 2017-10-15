from .base import Feature


class SecretBackendsFeature(Feature):
    def list(self):
        return self.client.get('/v1/sys/mounts').json()

    def mount(self, path, type, **kwargs):
        params = {
            'type': type,
        }
        params.update(kwargs)

        self.client.post('/v1/sys/mounts/{}'.format(path), json=params)

    def unmount(self, path):
        self.client.delete('/v1/sys/mounts/{}'.format(path))

    def remount(self, from_path, to_path):
        params = {
            'from': from_path,
            'to': to_path,
        }
        self.client.post('/v1/sys/remount', json=params)

    def get_config(self, path):
        return self.client.get('/v1/sys/mounts/{}/tune'.format(path)).json()

    def tune_config(self, path, **kwargs):
        self.client.post('/v1/sys/mounts/{}/tune'.format(path), json=kwargs)
