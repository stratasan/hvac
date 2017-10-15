def test_crud(client):
    client.auth_backends.mount('approle')

    try:
        ar = client.approle()

        ar.update_role('test', secret_id_num_uses=10)

        role = ar.role('test')
        assert role['data']['secret_id_num_uses'] == 10

        roles = ar.list_roles()
        assert 'test' in roles['data']['keys']

        ar.delete_role('test')
    finally:
        client.auth_backends.unmount('approle')
