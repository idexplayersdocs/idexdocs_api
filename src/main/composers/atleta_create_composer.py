from src.presentation.controllers.create_controler import CreateController
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_posicao import PosicaoRepo
from src.use_cases.atleta_create import AtletaCreateUseCase


def atleta_create_composer(data: dict, session):
    atleta_repository = AtletaRepo(session)
    posicao_repository = PosicaoRepo(session)

    use_case = AtletaCreateUseCase(
        atleta_repository=atleta_repository,
        posicao_repository=posicao_repository,
    )
    controller = CreateController(use_case=use_case)

    return controller.handle(data)
