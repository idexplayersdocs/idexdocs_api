from src.presentation.controllers.controle_delete_controler import (
    ControleDeleteController,
)
from src.repository.repo_controle import ControleRepo
from src.use_cases.controle_delete import ControleDeleteUseCase


def controle_delete_composer():
    controle_repository = ControleRepo()

    use_case = ControleDeleteUseCase(
        controle_repository=controle_repository
    )
    controller = ControleDeleteController(use_case=use_case)

    return controller.handle
