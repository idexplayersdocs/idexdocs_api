from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_lesao import LesaoRepo


class LesaoUpdateUseCase:
    def __init__(
        self,
        lesao_repository: LesaoRepo
    ):
        self.lesao_repository = lesao_repository

    def execute(self, http_request: HttpRequest):
        lesao_data: dict = dict(http_request.json)

        return self._update_lesao(lesao_data)

    def _update_lesao(self, lesao_data: dict):
        return self.lesao_repository.update_lesao(lesao_data)
