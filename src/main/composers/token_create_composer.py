from src.presentation.controllers.token_create_controler import (
    TokenCreateController,
)
from src.repository.repo_usuario import UsuarioRepo
from src.use_cases.token_create import TokenCreateUseCase


def token_create_composer():
    usuario_repository = UsuarioRepo()

    use_case = TokenCreateUseCase(usuario_repository=usuario_repository)
    controller = TokenCreateController(use_case=use_case)

    return controller.handle
