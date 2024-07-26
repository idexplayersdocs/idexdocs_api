from http import HTTPStatus


def test_create_atleta(client):
    response = client.post(
        '/atletas/',
        json={
            'nome': 'Atleta',
            'data_nascimento': '2000-01-01',
            'posicao_primaria': '7',
            'posicao_secundaria': '9',
            'posicao_terciaria': '10',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()


def test_list_atleta_empty(client):
    response = client.get('/atletas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == []


def test_list_atleta_full(client, atleta):
    response = client.get('/atletas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] != []


def test_update_atleta(client, atleta):
    response = client.put(
        f'/atletas/{atleta['id']}',
        json={
            'nome': 'Atleta',
            'data_nascimento': '2000-01-01',
            'posicao_primaria': '7',
            'posicao_secundaria': '9',
            'posicao_terciaria': '10',
            'ativo': False,
        },
    )

    assert response.status_code == HTTPStatus.OK
