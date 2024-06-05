from src.error.types.usuario_nao_encontrado import UsuarioNaoEncontrado
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_usuario import UsuarioRepo


class UsuarioUpdateUseCase:
    def __init__(self, usuario_repository: UsuarioRepo):
        self.usuario_repository = usuario_repository

    def execute(self, http_request: HttpRequest):
        usuario_data: dict = http_request.json
        usuario_id: int = usuario_data.get('id')

        self._check_usuario_by_id(usuario_id)

        return self._update_usuario(usuario_id, usuario_data)

    def _update_usuario(self, usuario_id: int, usuario_data: dict) -> dict:
        return self.usuario_repository.update_usuario(usuario_id, usuario_data)


    def _check_usuario_by_id(self, usuario_id: int):
        usuario = self.usuario_repository.get_usuario_by_id(usuario_id)

        if usuario is None:
            raise UsuarioNaoEncontrado('Usuário não encontrado')
