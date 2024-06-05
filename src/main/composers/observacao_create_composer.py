from src.presentation.controllers.obervacao_create_controler import (
    ObservacaoCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_observacao import ObservacaoRepo
from src.use_cases.observacao_create import ObservacaoCreateUseCase


def observacao_create_composer():
    observacao_repository = ObservacaoRepo()
    atleta_repository = AtletaRepo()

    use_case = ObservacaoCreateUseCase(
        observacao_repository, atleta_repository
    )
    controller = ObservacaoCreateController(use_case=use_case)

    return controller.handle
