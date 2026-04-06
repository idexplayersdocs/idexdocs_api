from src.presentation.controllers.contrato_update_controler import (
    ContratoUpdateController,
)
from src.repository.repo_contrato import ContratoRepo
from src.use_cases.contrato_update import ContratoUpdateUseCase


def contrato_update_composer():
    contrato_repository = ContratoRepo()

    use_case = ContratoUpdateUseCase(contrato_repository)
    controller = ContratoUpdateController(use_case=use_case)

    return controller.handle
