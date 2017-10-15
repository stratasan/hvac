import pytest

from .client import VaultClient
from .testutils import ServerManager


@pytest.fixture(scope='session')
def manager():
    return ServerManager('test/vault-tls.hcl')


@pytest.fixture(scope='session')
def client(manager):
    client = VaultClient(verify='test/server-cert.pem')
    manager.client = client

    manager.start()

    manager.initialize()
    manager.unseal()

    yield client

    manager.stop()
