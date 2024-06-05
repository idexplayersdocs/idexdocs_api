from src.presentation.controllers.clube_list_controler import (
    ClubeListController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_clube import ClubeRepo
from src.use_cases.clube_list import ClubeListUseCase


def clube_list_composer():
    clube_repository = ClubeRepo()
    atleta_repository = AtletaRepo()

    use_case = ClubeListUseCase(clube_repository, atleta_repository)
    controller = ClubeListController(use_case=use_case)

    return controller.handle
