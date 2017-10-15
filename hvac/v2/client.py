import requests

from hvac.exceptions import (Forbidden, InternalServerError,
    InvalidRequest, InvalidPath, VaultDown)

from .auditbackends import AuditBackendsFeature
from .authbackends import AuthBackendsFeature
from .leases import LeasesFeature
from .plugins import PluginsFeature
from .policies import PoliciesFeature
from .secretbackends import SecretBackendsFeature
from .sys import SysFeature
from .tokens import TokensFeature

from .auth.approle import AppRoleFeature
from .auth.userpass import UserPassFeature


class VaultClient:
    def __init__(self, base_url=None, token=None, cert=None, proxies=None,
                 timeout=10, verify=True):
        if not base_url:
            base_url = 'https://localhost:8200'

        self.base_url = base_url.rstrip('/')
        self.token = token

        self.audit_backends = AuditBackendsFeature(self)
        self.auth_backends = AuthBackendsFeature(self)
        self.leases = LeasesFeature(self)
        self.plugins = PluginsFeature(self)
        self.policies = PoliciesFeature(self)
        self.secret_backends = SecretBackendsFeature(self)
        self.sys = SysFeature(self)
        self.tokens = TokensFeature(self)

        self._wrap_lookup = None

        session = requests.Session()
        session.cert = cert
        session.proxies = proxies
        session.timeout = timeout
        session.verify = verify

        self.session = session

    def read(self, path):
        return self.get(self.normalize_path(path)).json()

    def list(self, path):
        params = dict(list=True)
        return self.get(self.normalize_path(path), params=params).json()

    def write(self, path, data):
        self.put(self.normalize_path(path), json=data)

    def delete(self, path):
        self.delete(self.normalize_path(path))

    def approle(self, mount_path='approle'):
        return AppRoleFeature(self, mount_path)

    def userpass(self, mount_path='userpass'):
        return UserPassFeature(self, mount_path)

    def wrap_lookup(self, func):
        self._wrap_lookup = func
        return func

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def request(self, method, url, headers=None, raise_for_status=True, wrap_ttl=None, **kwargs):
        if not headers:
            headers = {}

        if not wrap_ttl and self._wrap_lookup:
            _, path = url.split('/v1/', maxsplit=1)
            wrap_ttl = self._wrap_lookup(method, path)

        if wrap_ttl:
            headers['X-Vault-Wrap-TTL'] = str(wrap_ttl)

        if self.token:
            headers['X-Vault-Token'] = self.token

        if '://' not in url:
            url = '{}{}'.format(self.base_url, url)

        resp = self.session.request(method, url, headers=headers, **kwargs)
        if raise_for_status:
            self.raise_for_status(resp)

        return resp

    def raise_for_status(self, resp):
        if resp.status_code not in (200, 204):
            print(resp.status_code)

        if resp.status_code == 400:
            raise InvalidRequest(response=resp)
        if resp.status_code == 403:
            raise Forbidden(response=resp)
        if resp.status_code == 404:
            raise InvalidPath(response=resp)
        if resp.status_code == 500:
            raise InternalServerError(response=resp)
        if resp.status_code == 503:
            raise VaultDown(response=resp)

    def normalize_path(self, path):
        return '/v1/{}'.format(path.lstrip('/'))
