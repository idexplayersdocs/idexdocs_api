from src.presentation.controllers.controle_list_controler import (
    ControleListController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_controle import ControleRepo
from src.use_cases.controle_list import ControleListUseCase


def controle_list_composer():
    controle_repository = ControleRepo()
    atleta_repository = AtletaRepo()

    use_case = ControleListUseCase(
        controle_repository=controle_repository,
        atleta_repository=atleta_repository,
    )
    controller = ControleListController(use_case=use_case)

    return controller.handle
