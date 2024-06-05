from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_relacionamento import RelacionamentoRepo


class RelacionamentoListUseCase:
    def __init__(
        self,
        relacionamento_repository: RelacionamentoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.relacionamento_repository = relacionamento_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)

        total_count, result = self._list_relacionamentos(atleta_id, filters)
        return self._format_response(total_count, result)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_relacionamentos(self, atleta_id: int, filters: dict):
        relacionamentos = self.relacionamento_repository.list_relacionamento(
            atleta_id, filters
        )

        if len(relacionamentos) == 0:
            raise NotFoundError(
                'O Atleta não possui questionários cadastrados'
            )

        return relacionamentos

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Relacionamento',
            'data': result,
        }
