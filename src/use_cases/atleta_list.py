from src.error.types.credentials_exception import CredentialsException
from src.error.types.http_not_found import NotFoundError
from src.repository.repo_atleta import AtletaRepo


class AtletaListUseCase:
    def __init__(self, repository: AtletaRepo):
        self.repository = repository

    def execute(self, http_request: dict):
        filters: dict = http_request.copy()

        total_count, result = self._list_atletas(filters)
        return self._format_response(total_count, result)

    def _extract_token(self, authorization: str):
        token = (
            authorization.split(' ')[1]
            if authorization and ' ' in authorization
            else None
        )
        if not token:
            raise CredentialsException(
                'Não foi possível validar as credenciais'
            )
        return token

    def _list_atletas(self, filters):
        atletas = self.repository.list_atleta(filters)

        if len(atletas) == 0:
            raise NotFoundError('Não existem atletas cadastrados')

        return atletas

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Atleta',
            'data': result,
        }
