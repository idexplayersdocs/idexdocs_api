from src.presentation.controllers.usuario_update_controler import (
    UsuarioUpdateController,
)
from src.repository.repo_usuario import UsuarioRepo
from src.use_cases.usuario_update import UsuarioUpdateUseCase


def usuario_update_composer():
    usuario_repository = UsuarioRepo()

    use_case = UsuarioUpdateUseCase(usuario_repository=usuario_repository)
    controller = UsuarioUpdateController(use_case=use_case)

    return controller.handle
