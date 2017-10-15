def test_crud(client):
    client.auth_backends.mount('userpass')

    result = client.auth_backends.list()
    assert 'userpass/' in result['data']

    client.auth_backends.update_config('userpass', default_lease_ttl=86400)

    config = client.auth_backends.config('userpass')
    assert config['default_lease_ttl'] == 86400

    client.auth_backends.unmount('userpass')

    result = client.auth_backends.list()
    assert 'userpass/' not in result['data']
