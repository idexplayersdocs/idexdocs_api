from src.presentation.controllers.file_download_controler import (
    FileDownloadController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.file_download import FileDownloadUseCase


def file_download_composer():
    atleta_repository = AtletaRepo()

    use_case = FileDownloadUseCase(
        atleta_repository=atleta_repository,
    )
    controller = FileDownloadController(use_case=use_case)

    return controller.handle
