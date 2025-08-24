from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.file_upload_controler import (
    FileUploadController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_contrato import ContratoRepo
from src.repository.repo_controle import ControleRepo
from src.use_cases.file_upload import FileUploadUseCase


def file_upload_composer():
    atleta_repository = AtletaRepo()
    storage_service = AzureBlobStorage()
    controle_repository = ControleRepo()
    contrato_repository = ContratoRepo()

    use_case = FileUploadUseCase(
        atleta_repository=atleta_repository,
        storage_service=storage_service,
        controle_repository=controle_repository,
        contrato_repository=contrato_repository,
    )
    controller = FileUploadController(use_case=use_case)

    return controller.handle
