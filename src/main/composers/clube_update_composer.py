from src.presentation.controllers.clube_update_controler import (
    ClubeUpdateController,
)
from src.repository.repo_clube import ClubeRepo
from src.use_cases.clube_update import ClubeUpdateUseCase


def clube_update_composer():
    clube_repository = ClubeRepo()

    use_case = ClubeUpdateUseCase(
        clube_repository=clube_repository
    )
    controller = ClubeUpdateController(use_case=use_case)

    return controller.handle
