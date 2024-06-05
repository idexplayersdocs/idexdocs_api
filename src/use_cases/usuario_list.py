from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_usuario import UsuarioRepo


class UsuárioListUseCase:
    def __init__(self, usuario_repository: UsuarioRepo):
        self.usuario_repository = usuario_repository

    def execute(self, http_request: HttpRequest):
        filters: dict = dict(http_request.query_params.items())

        total_count, result = self._list_usuarios(filters)
        return self._format_response(total_count, result)

    def _list_usuarios(self, filters):
        usuarios = self.usuario_repository.list_usuario(filters)

        if len(usuarios) == 0:
            raise NotFoundError('Não existem atletas cadastrados')

        return usuarios

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Usuarios',
            'data': result,
        }
