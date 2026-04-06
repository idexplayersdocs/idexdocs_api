from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.files_delete_controler import (
    FileDeleteController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.file_docs_delete import DeleteFileDocsUseCase


def delete_file_docs_composer():
    storage_service = AzureBlobStorage()
    atleta_repository = AtletaRepo()

    use_case = DeleteFileDocsUseCase(
        storage_service=storage_service,
        atleta_repository=atleta_repository,
    )
    controller = FileDeleteController(use_case=use_case)

    return controller.handle
