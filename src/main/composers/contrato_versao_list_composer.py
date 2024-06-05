from src.presentation.controllers.contrato_list_controler import (
    ContratoListController,
)
from src.repository.repo_contrato import ContratoRepo
from src.use_cases.contrato_versao_list import ContratoVersaoListUseCase


def contrato_versao_list_composer():
    contrato_repository = ContratoRepo()

    use_case = ContratoVersaoListUseCase(contrato_repository)
    controller = ContratoListController(use_case=use_case)

    return controller.handle
