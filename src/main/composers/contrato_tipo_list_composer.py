from src.presentation.controllers.contrato_list_controler import (
    ContratoListController,
)
from src.repository.repo_contrato import ContratoRepo
from src.use_cases.contrato_tipo_list import ContratoTipoListUseCase


def contrato_tipo_list_composer():
    contrato_repository = ContratoRepo()

    use_case = ContratoTipoListUseCase(contrato_repository)
    controller = ContratoListController(use_case=use_case)

    return controller.handle
