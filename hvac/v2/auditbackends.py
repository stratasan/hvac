from .base import Feature


class AuditBackendsFeature(Feature):
    def list(self):
        return self.client.get('/v1/sys/audit').json()

    def mount(self, path, type, **kwargs):
        params = {
            'type': type,
        }
        params.update(kwargs)

        self.client.post('/v1/sys/audit/{}'.format(path), json=params)

    def unmount(self, path):
        self.client.delete('/v1/sys/audit/{}'.format(path))

    def hash(self, path, input, **kwargs):
        params = {
            'input': input,
        }
        params.update(kwargs)

        return self.client.post('/v1/sys/audit-hash/{}'.format(path), json=params).json()
