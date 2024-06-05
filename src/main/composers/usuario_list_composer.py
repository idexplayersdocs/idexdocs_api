from src.presentation.controllers.usuario_list_controler import (
    UsuarioListController,
)
from src.repository.repo_usuario import UsuarioRepo
from src.use_cases.usuario_list import UsuárioListUseCase


def usuario_list_composer():
    usuario_repository = UsuarioRepo()

    use_case = UsuárioListUseCase(usuario_repository=usuario_repository)
    controller = UsuarioListController(use_case=use_case)

    return controller.handle
