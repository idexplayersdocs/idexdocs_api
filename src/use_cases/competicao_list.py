from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_competicao import CompeticaoRepo


class CompeticaoListUseCase:
    def __init__(self, repository: CompeticaoRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        tota_count, result = self._list_competicao(atleta_id, filters)
        return self._format_response(tota_count, result)

    def _list_competicao(self, atleta_id: int, filters: dict):
        competicoes = self.repository.list_competicao(atleta_id, filters)

        if len(competicoes) == 0:
            raise NotFoundError('O Atleta não possui competições cadastradas')

        return competicoes

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Competição',
            'data': result,
        }
