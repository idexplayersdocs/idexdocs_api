from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_controle import ControleRepo


class ControleCreateUseCase:
    def __init__(
        self,
        controle_repository: ControleRepo,
        atleta_repository: AtletaRepo,
    ):
        self.controle_repository = controle_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        controle_data: dict = dict(http_request.json)

        atleta_id: int = controle_data.get('atleta_id')

        self._check_atleta_exists(atleta_id)

        return self._create_controle(controle_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _create_controle(self, controle_data: dict):
        controle = self.controle_repository.create_controle(controle_data)

        return controle
