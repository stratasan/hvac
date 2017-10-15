def test_health(client):
    health = client.sys.health()
    assert health['version']

def test_seal_unseal(client, manager):
    assert not client.sys.is_sealed()

    client.sys.seal()
    assert client.sys.is_sealed()

    manager.unseal()
    assert not client.sys.is_sealed()
