from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_clube import ClubeRepo
from src.repository.repo_contrato import ContratoRepo
from src.repository.repo_posicao import PosicaoRepo


class AtletaCreateUseCase:
    def __init__(
        self,
        atleta_repository: AtletaRepo,
        clube_repository: ClubeRepo,
        contrato_repository: ContratoRepo,
        posicao_repository: PosicaoRepo,
    ):
        self.atleta_repository = atleta_repository
        self.clube_repository = clube_repository
        self.contrato_repository = contrato_repository
        self.posicao_repository = posicao_repository

    def execute(self, http_request: HttpRequest):
        atleta_data: dict = http_request.json

        new_atleta: dict = self._create_atleta(atleta_data)
        atleta_data.update(new_atleta)

        self._create_clube(atleta_data)

        self._create_contrato(atleta_data)

        self._create_posicao(atleta_data)

        return new_atleta

    def _create_atleta(self, atleta_data: dict) -> dict:
        return self.atleta_repository.create_atleta(atleta_data)

    def _create_clube(self, atleta_data: dict):
        new_clube = atleta_data.get('clube')

        if new_clube['nome']:
            new_clube['atleta_id'] = atleta_data.get('id')

            return self.clube_repository.create_clube(new_clube)
        return None

    def _create_contrato(self, atleta_data: dict):
        new_contrato_clube = atleta_data.get('contrato_clube')
        new_contrato_empresa = atleta_data.get('contrato_empresa')

        if new_contrato_clube['contrato_sub_tipo_id']:
            new_contrato_clube['atleta_id'] = atleta_data.get('id')
            self.contrato_repository.create_contrato(new_contrato_clube)

        if new_contrato_empresa['contrato_sub_tipo_id']:
            new_contrato_empresa['atleta_id'] = atleta_data.get('id')
            self.contrato_repository.create_contrato(new_contrato_empresa)

    def _create_posicao(self, atleta_data: dict):
        def _get_value_or_none(key):
            value = atleta_data.get(key)
            return None if value == '' else value

        new_posicao = {
            'atleta_id': atleta_data.get('id'),
            'primeira': _get_value_or_none('posicao_primaria'),
            'segunda': _get_value_or_none('posicao_secundaria'),
            'terceira': _get_value_or_none('posicao_terciaria'),
        }

        return self.posicao_repository.create_posicao(new_posicao)
