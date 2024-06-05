from src.presentation.controllers.lesao_list_controler import (
    LesaoListController,
)
from src.repository.repo_lesao import LesaoRepo
from src.use_cases.lesao_list import LesaoListUseCase


def lesao_list_composer():
    repository = LesaoRepo()

    use_case = LesaoListUseCase(repository)
    controller = LesaoListController(use_case=use_case)

    return controller.handle
