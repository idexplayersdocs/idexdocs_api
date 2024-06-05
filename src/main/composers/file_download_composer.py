from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.file_download_controler import (
    FileDownloadController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.file_download import FileDownloadUseCase


def file_download_composer():
    atleta_repository = AtletaRepo()
    storage_service = AzureBlobStorage()

    use_case = FileDownloadUseCase(
        atleta_repository=atleta_repository,
        storage_service=storage_service,
    )
    controller = FileDownloadController(use_case=use_case)

    return controller.handle
