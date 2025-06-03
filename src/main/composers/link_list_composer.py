from src.presentation.controllers.link_list_controler import LinkListController
from src.repository.repo_links import LinkRepo
from src.use_cases.link_list import LinkListUseCase


def link_list_composer():
    link_repository = LinkRepo()

    use_case = LinkListUseCase(link_repository)
    controller = LinkListController(use_case=use_case)

    return controller.handle
