from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.controle_create_controler import (
    ControleCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_contrato import ContratoRepo
from src.repository.repo_controle import ControleRepo
from src.use_cases.controle_create import ControleCreateUseCase
from src.use_cases.file_upload import FileUploadUseCase


def controle_create_composer():
    controle_repository = ControleRepo()
    atleta_repository = AtletaRepo()
    contrato_repository = ContratoRepo()
    storage_service = AzureBlobStorage()

    file_upload_use_case = FileUploadUseCase(
        storage_service=storage_service,
        atleta_repository=atleta_repository,
        controle_repository=controle_repository,
        contrato_repository=contrato_repository,
    )

    use_case = ControleCreateUseCase(
        controle_repository=controle_repository,
        atleta_repository=atleta_repository,
        file_upload_use_case=file_upload_use_case,
    )
    controller = ControleCreateController(use_case=use_case)

    return controller.handle
