from src.presentation.controllers.atleta_create_controler import (
    AtletaCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_posicao import PosicaoRepo
from src.use_cases.atleta_create import AtletaCreateUseCase


def atleta_create_composer():
    atleta_repository = AtletaRepo()
    posicao_repository = PosicaoRepo()

    use_case = AtletaCreateUseCase(
        atleta_repository=atleta_repository,
        posicao_repository=posicao_repository,
    )
    controller = AtletaCreateController(use_case=use_case)

    return controller.handle
