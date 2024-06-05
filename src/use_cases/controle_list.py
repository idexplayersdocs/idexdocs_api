from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_controle import ControleRepo


class ControleListUseCase:
    def __init__(
        self,
        controle_repository: ControleRepo,
        atleta_repository: AtletaRepo,
    ):
        self.controle_repository = controle_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)

        total_count, result = self._list_controle(atleta_id, filters)
        return self._format_response(total_count, result)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_controle(self, atleta_id: int, filters: dict):
        controles = self.controle_repository.list_controle(atleta_id, filters)

        if len(controles) == 0:
            raise NotFoundError('O Atleta não possui controles cadastrados')

        return controles

    def _format_response(self, total_count: int, result: list[dict]) -> dict:

        total_sum = sum(item['preco'] for item in result)

        return {
            'count': len(result),
            'total': total_count,
            'type': 'Controle',
            'data': {'controles': result, 'total': total_sum},
        }
