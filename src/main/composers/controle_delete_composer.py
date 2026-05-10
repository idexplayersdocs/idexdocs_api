from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.controle_delete_controler import (
    ControleDeleteController,
)
from src.repository.repo_controle import ControleRepo
from src.use_cases.controle_delete import ControleDeleteUseCase


def controle_delete_composer():
    controle_repository = ControleRepo()
    storage_service = AzureBlobStorage()

    use_case = ControleDeleteUseCase(
        controle_repository=controle_repository,
        storage_service=storage_service,
    )
    controller = ControleDeleteController(use_case=use_case)

    return controller.handle
