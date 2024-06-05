from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.files_delete_controler import (
    FileDeleteController,
)
from src.repository.repo_arquivos import ArquivoRepo
from src.use_cases.files_delete import DeleteFilesUseCase


def delete_files_composer():
    storage_service = AzureBlobStorage()
    arquivo_repository = ArquivoRepo()

    use_case = DeleteFilesUseCase(
        storage_service=storage_service,
        arquivo_repository=arquivo_repository,
    )
    controller = FileDeleteController(use_case=use_case)

    return controller.handle
