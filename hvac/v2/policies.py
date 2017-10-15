from .base import Feature


class PoliciesFeature(Feature):
    def list(self):
        return self.client.get('/v1/sys/policy').json()

    def get(self, name):
        return self.client.get('/v1/sys/policy/{}'.format(name)).json()

    def update(self, name, rules, **kwargs):
        params = {
            'rules': rules,
        }
        params.update(kwargs)

        self.client.put('/v1/sys/policy/{}'.format(name), json=params)

    def delete(self, name):
        self.client.delete('/v1/sys/policy/{}'.format(name))
