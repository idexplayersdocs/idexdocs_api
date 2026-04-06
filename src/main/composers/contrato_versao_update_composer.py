from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.contrato_versao_update_controler import (
    ContratoVersaoUpdateController,
)
from src.repository.repo_contrato import ContratoRepo
from src.use_cases.contrato_versao_update import ContratoVersaoUpdateUseCase


def contrato_versao_update_composer():
    contrato_repository = ContratoRepo()
    storage_service = AzureBlobStorage()

    use_case = ContratoVersaoUpdateUseCase(
        contrato_repository=contrato_repository,
        storage_service=storage_service,
    )
    controller = ContratoVersaoUpdateController(use_case=use_case)

    return controller.handle
