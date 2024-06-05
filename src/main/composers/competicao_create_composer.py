from src.presentation.controllers.competicao_create_controler import (
    CompeticaoCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_competicao import CompeticaoRepo
from src.use_cases.competicao_create import CompeticaoCreateUseCase


def competicao_create_composer():
    competicao_repository = CompeticaoRepo()
    atleta_repository = AtletaRepo()

    use_case = CompeticaoCreateUseCase(
        competicao_repository=competicao_repository,
        atleta_repository=atleta_repository,
    )
    controller = CompeticaoCreateController(use_case=use_case)

    return controller.handle
