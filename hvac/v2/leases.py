from .base import Feature


class LeasesFeature(Feature):
    def get(self, lease_id):
        params = dict(lease_id=lease_id)
        return self.client.put('/v1/sys/leases/lookup', json=params).json()

    def list(self, prefix):
        params = dict(list=True)
        return self.client.get('/v1/sys/leases/lookup/{}'.format(prefix), params=params).json()

    def renew(self, lease_id, **kwargs):
        params = dict(lease_id=lease_id)
        params.update(kwargs)

        return self.client.put('/v1/sys/leases/renew', json=params).json()

    def revoke(self, lease_id):
        params = dict(lease_id=lease_id)
        self.client.put('/v1/sys/leases/revoke', json=params)

    def revoke_force(self, prefix):
        self.client.put('/v1/sys/leases/revoke-force/{}'.format(prefix))

    def revoke_prefix(self, prefix):
        self.client.put('/v1/sys/leases/revoke-prefix/{}'.format(prefix))
