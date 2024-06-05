from src.error.types.usuario_exists import UsuarioExistente
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_usuario import UsuarioRepo
from src.security import get_password_hash


class UsuarioCreateUseCase:
    def __init__(self, usuario_repository: UsuarioRepo):
        self.usuario_repository = usuario_repository

    def execute(self, http_request: HttpRequest):
        usuario_data: dict = http_request.json

        self._check_usuario_exists(usuario_data.get('email'))

        hashed_password = self._get_password_hash(usuario_data.get('password'))
        usuario_data.update({'hash_password': hashed_password})

        return self._create_usuario(usuario_data)

    def _create_usuario(self, usuario_data: dict) -> dict:
        return self.usuario_repository.create_usuario(usuario_data)

    def _get_password_hash(self, password: str) -> str:
        return get_password_hash(password)

    def _check_usuario_exists(self, usuario_email: str):
        usuario = self.usuario_repository.get_usuario_by_email(usuario_email)

        if usuario is not None:
            raise UsuarioExistente('Usuário já cadastrado')
