
from src.presentation.controllers.usuario_update_password_controler import (
    UsuarioUpdatePasswordController,
)
from src.repository.repo_usuario import UsuarioRepo
from src.use_cases.usuario_update_password import UsuarioUpdatePasswordUseCase


def usuario_update_password_composer():
    usuario_repository = UsuarioRepo()

    use_case = UsuarioUpdatePasswordUseCase(usuario_repository=usuario_repository)
    controller = UsuarioUpdatePasswordController(use_case=use_case)

    return controller.handle
