from http import HTTPStatus


def test_create_clube(client, atleta):
    response = client.post(
        '/clubes/',
        json={
            'atleta_id': atleta['id'],
            'nome': 'Clube',
            'data_inicio': '2000-01-01',
            'data_fim': '2000-01-01',
            'clube_atual': True
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_list_clube(client, atleta):
    response = client.get(f'/clubes/{atleta['id']}')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == []