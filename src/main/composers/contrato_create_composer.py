from src.presentation.controllers.contrato_create_controler import (
    ContratoCreateController,
)
from src.repository.repo_contrato import ContratoRepo
from src.use_cases.contrato_create import ContratoCreateUseCase


def contrato_create_composer():
    contrato_repository = ContratoRepo()

    use_case = ContratoCreateUseCase(contrato_repository)
    controller = ContratoCreateController(use_case=use_case)

    return controller.handle
