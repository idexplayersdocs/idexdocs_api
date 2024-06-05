from src.presentation.controllers.lesao_create_controler import (
    LesaoCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_lesao import LesaoRepo
from src.use_cases.lesao_create import LesaoCreateUseCase


def lesao_create_composer():
    lesao_repository = LesaoRepo()
    atleta_repository = AtletaRepo()

    use_case = LesaoCreateUseCase(lesao_repository, atleta_repository)
    controller = LesaoCreateController(use_case=use_case)

    return controller.handle
