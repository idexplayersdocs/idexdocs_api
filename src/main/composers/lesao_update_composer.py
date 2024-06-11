from src.presentation.controllers.lesao_update_controler import (
    LesaoUpdateController,
)
from src.repository.repo_lesao import LesaoRepo
from src.use_cases.lesao_update import LesaoUpdateUseCase


def lesao_update_composer():
    lesao_repository = LesaoRepo()

    use_case = LesaoUpdateUseCase(lesao_repository)
    controller = LesaoUpdateController(use_case=use_case)

    return controller.handle
