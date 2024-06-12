from src.error.types.clube_ativo import ClubeAtivoExistente
from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_clube import ClubeRepo


class ClubeCreateUseCase:
    def __init__(
        self,
        clube_repository: ClubeRepo,
        atleta_repository: AtletaRepo,
    ):
        self.clube_repository = clube_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        clube_data: dict = dict(http_request.json)
        atleta_id: int = clube_data.get('atleta_id')
        clube_atual: bool = clube_data.get('clube_atual')

        self._check_atleta_exists(atleta_id)

        if clube_atual is True:
            self._check_clube_ativo_exists(atleta_id)

        return self._create_clube(clube_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _check_clube_ativo_exists(self, atleta_id: int):
        _, clubes = self.clube_repository.list_clube(atleta_id)

        for clube in clubes:
            if clube['clube_atual'] is True:
                raise ClubeAtivoExistente(
                    'O atleta já possui clube ativo. Inative antes de criar um novo.'
                )

    def _create_clube(self, clube_data: dict):
        return self.clube_repository.create_clube(clube_data)
