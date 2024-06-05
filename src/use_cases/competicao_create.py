from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_competicao import CompeticaoRepo


class CompeticaoCreateUseCase:
    def __init__(
        self,
        competicao_repository: CompeticaoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.competicao_repository = competicao_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        competicao_data: dict = dict(http_request.json)

        atleta_id: int = competicao_data.get('atleta_id')

        self._check_atleta_exists(atleta_id)

        return self._create_competicao(competicao_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _create_competicao(self, competicao_data: dict):
        competicao = self.competicao_repository.create_competicao(
            competicao_data
        )

        return competicao
