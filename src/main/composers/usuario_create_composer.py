from src.presentation.controllers.usuario_create_controler import (
    UsuarioCreateController,
)
from src.repository.repo_usuario import UsuarioRepo
from src.use_cases.usuario_create import UsuarioCreateUseCase


def usuario_create_composer():
    usuario_repository = UsuarioRepo()

    use_case = UsuarioCreateUseCase(usuario_repository=usuario_repository)
    controller = UsuarioCreateController(use_case=use_case)

    return controller.handle
