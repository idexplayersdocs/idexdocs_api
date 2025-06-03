from src.presentation.controllers.link_create_controler import (
    LinkCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_links import LinkRepo
from src.use_cases.link_create import LinkCreateUseCase


def link_create_composer():
    link_repository = LinkRepo()
    atleta_repository = AtletaRepo()

    use_case = LinkCreateUseCase(link_repository, atleta_repository)
    controller = LinkCreateController(use_case=use_case)

    return controller.handle
