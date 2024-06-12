from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_clube import ClubeRepo


class ClubeUpdateUseCase:
    def __init__(
        self,
        clube_repository: ClubeRepo,
    ):
        self.clube_repository = clube_repository

    def execute(self, http_request: HttpRequest):
        clube_data: dict = dict(http_request.json)

        return self._update_clube(clube_data)

    def _update_clube(self, clube_data: dict):
        return self.clube_repository.update_clube(clube_data)
