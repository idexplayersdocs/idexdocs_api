from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_clube import ClubeRepo


class ClubeListUseCase:
    def __init__(
        self,
        clube_repository: ClubeRepo,
        atleta_repository: AtletaRepo,
    ):
        self.clube_repository = clube_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)

        total_count, result = self._list_clube(atleta_id, filters)
        return self._format_response(total_count, result)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_clube(self, atleta_id: int, filters: dict):
        clubes = self.clube_repository.list_clube(atleta_id, filters)

        if len(clubes) == 0:
            raise NotFoundError('O Atleta não possui clubes cadastradas')

        return clubes

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Clubes',
            'data': result,
        }
