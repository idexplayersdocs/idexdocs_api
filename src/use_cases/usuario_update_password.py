from src.error.types.senha_invalida import SenhaInvalida
from src.error.types.usuario_nao_encontrado import UsuarioNaoEncontrado
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_usuario import UsuarioRepo
from src.security import get_password_hash, verify_password


class UsuarioUpdatePasswordUseCase:
    def __init__(self, usuario_repository: UsuarioRepo):
        self.usuario_repository = usuario_repository

    def execute(self, http_request: HttpRequest):
        usuario_data: dict = http_request.json
        usuario_id: int = usuario_data.get('id')
        new_password: str = usuario_data.get('new_password')
        old_password: str = usuario_data.pop('password')

        usuario = self._get_usuario_by_id(usuario_id)
        password_verified = self._verify_password(old_password, usuario.get('hash_password'), new_password)

        return self._update_usuario_password(usuario_id, password_verified)

    def _update_usuario_password(self, usuario_id: int, new_password: str) -> dict:
        return self.usuario_repository.update_usurio_password(usuario_id, new_password)

    def _get_usuario_by_id(self, usuario_id: int):
        usuario = self.usuario_repository.get_usuario_by_id(usuario_id)

        if usuario is None:
            raise UsuarioNaoEncontrado('Usuário não encontrado')
        
        return usuario
    
    def _verify_password(self, old_password: str, present_password: str, new_password: str):
        is_valid = verify_password(old_password, present_password)

        if not is_valid:
            raise SenhaInvalida('Senha invalida')

        return self._get_password_hash(new_password)
        
    def _get_password_hash(self, password: str) -> str:
        return get_password_hash(password)