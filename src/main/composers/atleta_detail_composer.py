from src.presentation.controllers.atleta_detail_controler import (
    AtletaDetailController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.atleta_detail import AtletaDetailUseCase


def atleta_detail_composer():
    repository = AtletaRepo()
    use_case = AtletaDetailUseCase(repository=repository)
    controller = AtletaDetailController(use_case=use_case)

    return controller.handle
