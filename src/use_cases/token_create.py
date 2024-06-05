from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_usuario import UsuarioRepo
from src.security.security import login_user


class TokenCreateUseCase:
    def __init__(self, usuario_repository: UsuarioRepo) -> None:
        self.usuario_repository = usuario_repository

    def execute(self, http_request: HttpRequest):
        login_data: dict = http_request.json
        email: str = login_data.get('email')
        password: str = login_data.get('password')

        return login_user(email, password)
