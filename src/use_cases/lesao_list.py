from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_lesao import LesaoRepo


class LesaoListUseCase:
    def __init__(self, repository: LesaoRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        total_count, result = self._list_lesao(atleta_id, filters)
        return self._format_response(total_count, result)

    def _list_lesao(self, atleta_id: int, filters: dict):
        lesoes = self.repository.list_lesao(atleta_id, filters)

        if len(lesoes) == 0:
            raise NotFoundError('O Atleta não possui lesões cadastradas')

        return lesoes

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Lesão',
            'data': result,
        }
