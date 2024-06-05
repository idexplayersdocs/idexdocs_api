from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_contrato import ContratoRepo


class ContratoListUseCase:
    def __init__(self, contrato_repository: ContratoRepo):
        self.contrato_repository = contrato_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        total_count, result = self._list_contrato(atleta_id, filters)
        return self._format_response(total_count, result)

    def _list_contrato(self, atleta_id: int, filters: dict):
        contratos = self.contrato_repository.list_contrato(atleta_id, filters)

        if len(contratos) == 0:
            raise NotFoundError('O Atleta não possui contratos cadastrados')

        return contratos

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Contratos',
            'data': result,
        }
