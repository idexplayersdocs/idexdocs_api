import logging

from azure.core.exceptions import ResourceNotFoundError

from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_controle import ControleRepo

logger = logging.getLogger(__name__)


class ControleDeleteUseCase:

    CONTAINER_NAME = 'atleta-controles'

    def __init__(
        self,
        controle_repository: ControleRepo,
        storage_service: AzureBlobStorage,
    ):
        self.controle_repository = controle_repository
        self.storage_service = storage_service

    def execute(self, http_request: HttpRequest):
        controle_id: int = http_request.path_params.get('id')
        return self._delete_controle(controle_id)

    def _delete_controle(self, controle_id: int):
        # 1. Fetch linked avatars (blob URLs) before any deletion
        avatars = self.controle_repository.get_avatars_by_controle_id(controle_id)

        # 2. Delete blobs from Azure (missing blobs are logged, not fatal)
        for avatar in avatars:
            self._delete_blob(avatar.blob_url)

        # 3. Delete AtletaAvatar DB rows + HistoricoControle atomically
        return self.controle_repository.delete_controle(controle_id)

    def _delete_blob(self, blob_url: str) -> None:
        blob_name = self._extrair_blob_path_name(self.CONTAINER_NAME, blob_url)
        try:
            self.storage_service.delete_imagem(self.CONTAINER_NAME, blob_name)
        except ResourceNotFoundError:
            logger.warning(
                'Blob not found in Azure, skipping: container=%s blob=%s',
                self.CONTAINER_NAME,
                blob_name,
            )

    def _extrair_blob_path_name(self, container: str, blob_url: str) -> str:
        parts = blob_url.split(container)
        result = parts[1] if len(parts) > 1 else ''
        return result[1:]  # strip leading slash
