from src.presentation.controllers.link_delete_controler import (
    LinkDeleteController,
)
from src.repository.repo_links import LinkRepo
from src.use_cases.link_delete import LinkDeleteUseCase


def link_delete_composer():
    link_repository = LinkRepo()

    use_case = LinkDeleteUseCase(link_repository)
    controller = LinkDeleteController(use_case=use_case)

    return controller.handle
