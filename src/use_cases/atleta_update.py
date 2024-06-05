from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class AtletaUpdateUseCase:
    def __init__(self, atleta_repository: AtletaRepo):
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_data: dict = http_request.json
        atleta_id: int = int(http_request.path_params.get('id'))
        
        result = self._update_atleta(atleta_id, atleta_data)

        return result

    def _update_atleta(self, atleta_id: int, atleta_data: dict) -> dict:
        return self.atleta_repository.update_atleta(atleta_id, atleta_data)
