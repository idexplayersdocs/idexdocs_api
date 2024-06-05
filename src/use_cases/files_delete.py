from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_arquivos import ArquivoRepo


class DeleteFilesUseCase:

    CONTAINER_NAME = 'atleta-imagens'

    def __init__(
        self,
        storage_service: AzureBlobStorage,
        arquivo_repository: ArquivoRepo,
    ):
        self.storage_service = storage_service
        self.arquivo_repository = arquivo_repository

    def execute(self, http_request: HttpRequest):
        imagem_id: int = http_request.path_params.get('id')

        blob = self._get_imagem_blob(imagem_id)
        self._delete_blob_assets(self.CONTAINER_NAME, blob)
        return self.arquivo_repository.delete_imagem(imagem_id)

    def _get_imagem_blob(self, imagem_id: int):
        blob = self.arquivo_repository.get_imagem_by_id(imagem_id)
        if blob is None:
            raise NotFoundError('Imagem não encontrada')
        return blob

    def _delete_blob_assets(self, container, blob):
        blob_name = self._extrair_blob_path_name(container, blob.blob_url)
        self.storage_service.delete_imagem(container, blob_name)

    def _extrair_blob_path_name(self, container: str, blob_url: str) -> str:
        delimiter = container
        # Split the URL based on the delimiter
        parts = blob_url.split(delimiter)

        # Retrieve everything to the right of the delimiter
        result = parts[1] if len(parts) > 1 else ''

        # Remove leading slash
        return result[1:]
