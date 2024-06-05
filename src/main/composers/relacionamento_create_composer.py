from src.presentation.controllers.relacionamento_create_controler import (
    RelacionamentoCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_relacionamento import RelacionamentoRepo
from src.use_cases.relacionamento_create import RelacionamentoCreateUseCase


def relacionamento_create_composer():
    relacionamento_repository = RelacionamentoRepo()
    atleta_repository = AtletaRepo()

    use_case = RelacionamentoCreateUseCase(
        relacionamento_repository=relacionamento_repository,
        atleta_repository=atleta_repository,
    )
    controller = RelacionamentoCreateController(use_case=use_case)

    return controller.handle
