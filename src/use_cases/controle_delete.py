from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_controle import ControleRepo


class ControleDeleteUseCase:
    def __init__(
        self,
        controle_repository: ControleRepo,
    ):
        self.controle_repository = controle_repository

    def execute(self, http_request: HttpRequest):
        controle_id: int = http_request.path_params.get('id')

        return self._delete_controle(controle_id)

    def _delete_controle(self, controle_id: int):
        controle_id = self.controle_repository.delete_controle(
            controle_id
        )

        return controle_id
