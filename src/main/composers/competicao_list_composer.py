from src.presentation.controllers.competicao_list_controler import (
    CompeticaoListController,
)
from src.repository.repo_competicao import CompeticaoRepo
from src.use_cases.competicao_list import CompeticaoListUseCase


def competicao_list_composer():
    repository = CompeticaoRepo()

    use_case = CompeticaoListUseCase(repository)
    controller = CompeticaoListController(use_case=use_case)

    return controller.handle
