from src.presentation.controllers.relacionamento_list_controler import (
    RelacionamentoListController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_relacionamento import RelacionamentoRepo
from src.use_cases.relacionamento_list import RelacionamentoListUseCase


def relacionamento_list_composer():
    relacionamento_repository = RelacionamentoRepo()
    atleta_repository = AtletaRepo()

    use_case = RelacionamentoListUseCase(
        relacionamento_repository=relacionamento_repository,
        atleta_repository=atleta_repository,
    )
    controller = RelacionamentoListController(use_case=use_case)

    return controller.handle
