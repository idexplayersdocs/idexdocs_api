from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class FileDownloadUseCase:
    def __init__(
        self, atleta_repository: AtletaRepo, storage_service: AzureBlobStorage
    ):
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository
        self.file_name = 'atleta-avatar'

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get('id')

        self._check_atleta_exists(atleta_id)
        blob_url = self._get_blob_url(atleta_id)

        return self._format_response(blob_url)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _get_blob_url(self, atleta_id: int):
            return self.atleta_repository.get_blob_url(atleta_id)
    
    def _format_response(self, blob_url: str | None):
        return {'status': bool(blob_url), 'blob_url': blob_url}
         
