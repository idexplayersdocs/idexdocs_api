from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_competicao import CompeticaoRepo


class CompeticaoUpdateUseCase:
    def __init__(self, competicao_repository: CompeticaoRepo):
        self.competicao_repository = competicao_repository

    def execute(self, http_request: HttpRequest):
        competicao_data: dict = dict(http_request.json)

        return self._update_competicao(competicao_data)

    def _update_competicao(self, competicao_data: dict):
        return self.competicao_repository.update_competicao(competicao_data)
