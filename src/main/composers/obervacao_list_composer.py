from src.presentation.controllers.obervacao_list_controler import (
    ObservacaoListController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_observacao import ObservacaoRepo
from src.use_cases.observacao_list import ObservacaoListUseCase


def observacao_list_composer():
    observacao_repository = ObservacaoRepo()
    atleta_repository = AtletaRepo()

    use_case = ObservacaoListUseCase(observacao_repository, atleta_repository)
    controller = ObservacaoListController(use_case=use_case)

    return controller.handle
