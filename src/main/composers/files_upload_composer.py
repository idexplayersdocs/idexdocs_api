from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.files_upload_controler import (
    MultipleFilesUploadController,
)
from src.repository.repo_arquivos import ArquivoRepo
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.files_upload import MultipleFilesUploadUseCase


def multiple_files_upload_composer():
    atleta_repository = AtletaRepo()
    storage_service = AzureBlobStorage()
    arquivos_repository = ArquivoRepo()

    use_case = MultipleFilesUploadUseCase(
        atleta_repository=atleta_repository,
        storage_service=storage_service,
        arquivo_repository=arquivos_repository
    )
    controller = MultipleFilesUploadController(use_case=use_case)

    return controller.handle
