from .base import Feature


class SysFeature(Feature):
    def health(self):
        return self.client.get('/v1/sys/health', raise_for_status=False).json()

    def leader(self):
        return self.client.get('/v1/sys/leader').json()

    def wrap(self, data, ttl):
        return self.client.post('/v1/sys/wrapping/wrap', json=data, wrap_ttl=ttl).json()

    def rewrap(self, token):
        params = dict(token=token)
        return self.client.post('/v1/sys/wrapping/rewrap', json=params).json()

    def unwrap(self, token):
        params = dict(token=token)
        return self.client.post('/v1/sys/wrapping/unwrap', json=params).json()

    def lookup_wrap(self, token):
        params = dict(token=token)
        return self.client.post('/v1/sys/wrapping/lookup', json=params).json()

    def is_initialized(self):
        result = self.client.get('/v1/sys/init').json()
        return result['initialized']

    def init(self, secret_shares=5, secret_threshold=3, **kwargs):
        params = {
            'secret_shares': secret_shares,
            'secret_threshold': secret_threshold,
        }
        params.update(kwargs)

        return self.client.put('/v1/sys/init', json=params).json()

    def seal_status(self):
        return self.client.get('/v1/sys/seal-status').json()

    def is_sealed(self):
        status = self.seal_status()
        return status['sealed']

    def seal(self):
        self.client.put('/v1/sys/seal')

    def unseal(self, key=None, **kwargs):
        params = {
            'key': key,
        }
        params.update(kwargs)

        return self.client.put('/v1/sys/unseal', json=params).json()

    def unseal_multi(self, keys):
        last_result = None
        for key in keys:
            last_result = self.unseal(key)
            if not last_result['sealed']:
                break

        return last_result

    def step_down(self):
        self.client.put('/v1/sys/step-down')

    def key_status(self):
        return self.client.get('/v1/sys/key-status').json()

    def rotate(self):
        self.client.put('/v1/sys/rotate')

    def rekey(self):
        return self.client.get('/v1/sys/rekey/init').json()

    def start_rekey(self, secret_shares=5, secret_threshold=3, **kwargs):
        params = {
            'secret_shares': secret_shares,
            'secret_threshold': secret_threshold,
        }
        params.update(kwargs)

        self.client.put('/v1/sys/rekey/init', json=params)

    def cancel_rekey(self):
        self.client.delete('/v1/sys/rekey/init')

    def backup_key(self):
        return self.client.get('/v1/sys/rekey/backup').json()

    def delete_backup_key(self):
        self.client.delete('/v1/sys/rekey/backup')

    def update_rekey(self, key, nonce):
        params = {
            'key': key,
            'nonce': nonce,
        }

        return self.client.put('/v1/sys/rekey/update', json=params).json()

    def generate_root_status(self):
        return self.client.get('/v1/sys/generate-root/attempt').json()

    def start_root_generation(self, **kwargs):
        return self.client.put('/v1/sys/generate-root/attempt', json=kwargs).json()

    def cancel_root_generation(self):
        self.client.delete('/v1/sys/generate-root/attempt')

    def update_root_generation(self, key, nonce):
        params = {
            'key': key,
            'nonce': nonce,
        }
        return self.client.put('/v1/sys/generate-root/update', json=params).json()

    def cors_config(self):
        return self.client.get('/v1/sys/config/cors').json()

    def update_cors_config(self, allowed_origins, **kwargs):
        params = {
            'allowed_origins': allowed_origins,
        }
        params.update(kwargs)

        self.client.put('/v1/sys/config/cors', json=params)

    def clear_cors_config(self):
        self.client.delete('/v1/sys/config/cors')

    def capabilities(self, path, token=None):
        if not token:
            token = self.client.token

        params = {
            'path': path,
            'token': token,
        }
        return self.client.post('/v1/sys/capabilities', json=params).json()

    def capabilities_accessor(self, path, accessor):
        params = {
            'path': path,
            'accessor': accessor,
        }
        return self.client.post('/v1/sys/capabilities-accessor', json=params).json()
