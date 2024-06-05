from src.presentation.controllers.atleta_create_controler import (
    AtletaCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_clube import ClubeRepo
from src.repository.repo_contrato import ContratoRepo
from src.repository.repo_posicao import PosicaoRepo
from src.use_cases.atleta_create import AtletaCreateUseCase


def atleta_create_composer():
    atleta_repository = AtletaRepo()
    clube_repository = ClubeRepo()
    contrato_repository = ContratoRepo()
    posicao_repository = PosicaoRepo()

    use_case = AtletaCreateUseCase(
        atleta_repository=atleta_repository,
        clube_repository=clube_repository,
        contrato_repository=contrato_repository,
        posicao_repository=posicao_repository,
    )
    controller = AtletaCreateController(use_case=use_case)

    return controller.handle
