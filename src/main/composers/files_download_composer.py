from src.presentation.controllers.file_download_controler import (
    FileDownloadController,
)
from src.repository.repo_arquivos import ArquivoRepo
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.files_download import MultipleFilesDownloadUseCase


def multiple_files_download_composer():
    atleta_repository = AtletaRepo()
    arquivo_repository = ArquivoRepo()

    use_case = MultipleFilesDownloadUseCase(
        atleta_repository=atleta_repository,
        arquivo_repository=arquivo_repository,
    )
    controller = FileDownloadController(use_case=use_case)

    return controller.handle
