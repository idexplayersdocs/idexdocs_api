from collections import OrderedDict
from datetime import date, datetime

from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_posicao import PosicaoRepo


class AtletaCreateUseCase:
    def __init__(
        self,
        atleta_repository: AtletaRepo,
        posicao_repository: PosicaoRepo,
    ):
        self.atleta_repository = atleta_repository
        self.posicao_repository = posicao_repository

    def execute(self, http_request: HttpRequest):
        atleta_data: dict = http_request

        new_atleta: dict = self._create_atleta(atleta_data)
        atleta_data.update(new_atleta)

        self._create_posicao(atleta_data)

        return new_atleta

    def _create_atleta(self, atleta_data: dict) -> dict:
        date_obj: date = datetime.strptime(
            atleta_data.get('data_nascimento'), '%Y-%m-%d'
            )
        atleta_data['data_nascimento'] = date_obj
        return self.atleta_repository.create_atleta(atleta_data)

    def _create_posicao(self, atleta_data: dict):

        new_posicao = OrderedDict(
            [
                ('atleta_id', atleta_data.get('id')),
                ('primeira', int(atleta_data.get('posicao_primaria'))),
                ('segunda', int(atleta_data.get('posicao_secundaria'))),
                ('terceira', int(atleta_data.get('posicao_terciaria'))),
            ]
        )

        return self.posicao_repository.create_posicao(new_posicao)
