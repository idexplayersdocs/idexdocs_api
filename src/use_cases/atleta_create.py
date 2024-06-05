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
        posicao_repository: PosicaoRepo
    ):
        self.atleta_repository = atleta_repository
        self.clube_repository = clube_repository
        self.contrato_repository = contrato_repository
        self.posicao_repository = posicao_repository

    def execute(self, http_request: HttpRequest):
        atleta_data: dict = http_request.json
        new_atleta: dict = self._create_atleta(atleta_data)
        atleta_data.update(new_atleta)

        new_clube = self._create_clube(atleta_data)

        new_contrato = self._create_contrato(atleta_data)

        new_posicao = self._create_posicao(atleta_data)

        return new_atleta and new_clube and new_contrato and new_posicao

    def _create_atleta(self, atleta_data: dict) -> dict:
        return self.atleta_repository.create_atleta(atleta_data)
    
    def _create_clube(self, atleta_data: dict):
        new_clube = atleta_data.get('clube')
        new_clube['atleta_id'] = atleta_data.get('id')

        return self.clube_repository.create_clube(new_clube)

    def _create_contrato(self, atleta_data: dict):
        new_contrato_clube = atleta_data.get('contrato_clube')
        new_contrato_clube['atleta_id'] = atleta_data.get('id')

        new_contrato_empresa = atleta_data.get('contrato_empresa')
        new_contrato_empresa['atleta_id'] = atleta_data.get('id')
        
        clube = self.contrato_repository.create_contrato(new_contrato_clube)
        empresa = self.contrato_repository.create_contrato(new_contrato_empresa)
        return clube and empresa

    def _create_posicao(self, atleta_data: dict):
        new_posicao = {}
        new_posicao['atleta_id'] = atleta_data.get('id')
        new_posicao['primeira'] = atleta_data.get('posicao_primaria')
        new_posicao['segunda'] = atleta_data.get('posicao_secundaria')
        new_posicao['terceira'] = atleta_data.get('posicao_terciaria')

        return self.posicao_repository.create_posicao(new_posicao)



