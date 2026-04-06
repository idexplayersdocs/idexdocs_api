from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.contrato_versao_create_controler import (
    ContratoVersaoCreateController,
)
from src.repository.repo_contrato import ContratoRepo
from src.use_cases.contrato_versao_create import ContratoVersaoCreateUseCase


def contrato_versao_create_composer():
    contrato_repository = ContratoRepo()
    storage_service = AzureBlobStorage()

    use_case = ContratoVersaoCreateUseCase(
        contrato_repository=contrato_repository,
        storage_service=storage_service,
    )
    controller = ContratoVersaoCreateController(use_case=use_case)

    return controller.handle
