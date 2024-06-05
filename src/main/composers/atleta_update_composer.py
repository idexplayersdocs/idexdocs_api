from src.presentation.controllers.atleta_update_controler import (
    AtletaUpdateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.atleta_update import AtletaUpdateUseCase


def atleta_update_composer():
    atleta_repository = AtletaRepo()
    use_case = AtletaUpdateUseCase(atleta_repository=atleta_repository)
    controller = AtletaUpdateController(use_case=use_case)

    return controller.handle
