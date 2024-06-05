from src.presentation.controllers.controle_create_controler import (
    ControleCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_controle import ControleRepo
from src.use_cases.controle_create import ControleCreateUseCase


def controle_create_composer():
    controle_repository = ControleRepo()
    atleta_repository = AtletaRepo()

    use_case = ControleCreateUseCase(
        controle_repository=controle_repository,
        atleta_repository=atleta_repository,
    )
    controller = ControleCreateController(use_case=use_case)

    return controller.handle
