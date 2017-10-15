from .base import Feature


class PluginsFeature(Feature):
    def list(self):
        params = dict(params=True)
        return self.client.get('/v1/sys/plugins/catalog', params=params).json()

    def register(self, name, sha256, command, **kwargs):
        params = {
            'sha256': sha256,
            'command': command,
        }
        params.update(kwargs)

        self.client.post('/v1/sys/plugins/catalog/{}'.format(name), json=params)

    def get(self, name):
        return self.client.get('/v1/sys/plugins/catalog/{}'.format(name)).json()

    def remove(self, name):
        self.client.delete('/v1/sys/plugins/catalog/{}'.format(name))

    def reload(self, plugin=None, mounts=None, **kwargs):
        params = {}
        if plugin:
            params['plugin'] = plugin
        if mounts:
            params['mounts'] = mounts

        params.update(kwargs)

        self.client.put('/v1/sys/plugins/reload/backend', json=params)
