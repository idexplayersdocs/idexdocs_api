from src.presentation.controllers.competicao_update_controler import (
    CompeticaoUpdateController,
)
from src.repository.repo_competicao import CompeticaoRepo
from src.use_cases.competicao_update import CompeticaoUpdateUseCase


def competicao_update_composer():
    competicao_repository = CompeticaoRepo()

    use_case = CompeticaoUpdateUseCase(
        competicao_repository=competicao_repository
    )
    controller = CompeticaoUpdateController(use_case=use_case)

    return controller.handle
