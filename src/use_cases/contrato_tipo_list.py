from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_contrato import ContratoRepo


class ContratoTipoListUseCase:
    def __init__(self, contrato_repository: ContratoRepo):
        self.contrato_repository = contrato_repository

    def execute(self, http_request: HttpRequest):

        result = self._list_contrato_tipo()
        return self._format_response(result)

    def _list_contrato_tipo(self):
        return self.contrato_repository.list_contrato_tipo()

    def _format_response(self, result: list[dict]) -> dict:
        return {
            'type': 'ContratoTipo',
            'data': result,
        }
