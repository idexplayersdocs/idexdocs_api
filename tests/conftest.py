import datetime

import factory
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from asgi import app
from src.database import session_context
from src.repository.model_objects import Atleta, AtletaPosicao

# def datetime_now_sec():
#     return datetime.now().replace(microsecond=0)


# class AtletaFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = Atleta
#         sqlalchemy_session_persistence = 'commit'

#     id = factory.Sequence(lambda n: n)
#     nome = factory.Faker('name')
#     data_nascimento = factory.Faker('date_of_birth')
#     data_criacao = factory.LazyFunction(datetime_now_sec)
#     data_atualizado = None
#     ativo = True


# class AtletaPosicaoFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = AtletaPosicao
#         sqlalchemy_session_persistence = 'commit'

#     atleta_id = factory.SubFactory(AtletaFactory)
#     posicao_id = factory.Sequence(lambda n: n)
#     preferencia = factory.Faker('word')
#     data_criacao = factory.LazyFunction(datetime_now_sec)
#     data_atualizado = None

#     atleta = factory.RelatedFactory(
#         AtletaFactory, factory_related_name='posicoes'
#     )


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        # Especificações do SQLite
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[session_context] = get_session_override

        yield client


@pytest.fixture()
def atleta(client):
    response = client.post(
        '/atletas/',
        json={
            'nome': 'Atleta',
            'data_nascimento': '2000-01-01',
            'posicao_primaria': '1',
            'posicao_secundaria': '9',
            'posicao_terciaria': '10',
        },
    )

    return response.json()
