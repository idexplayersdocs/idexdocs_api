from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class DeleteFileDocsUseCase:
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        atleta_repository: AtletaRepo,
    ):
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        file_id: int = http_request.path_params.get('id')
        original_resource_path: str = http_request.url.path.split('/')[-2]

        if original_resource_path == 'recibo':
            resource_path = 'controles'
        elif original_resource_path == 'contrato':
            resource_path = 'contratos'

        file = self._get_file_uri(file_id)
        blob_name = file.blob_url.split('/')[-1]
        container_name: str = 'atleta-' + resource_path

        if self._delete_blob_assets(container_name, blob_name) is True:
            print('Arquivo deletado com sucesso', flush=True)
            return self.atleta_repository.delete_blob_url(file_id)
        return False

    def _get_file_uri(self, file_id: int):
        uri = self.atleta_repository.get_blob_by_id(file_id)
        if uri is None:
            raise NotFoundError('Arquivo não encontrado')
        return uri

    def _delete_blob_assets(self, container, uri) -> bool:
        try:
            self.storage_service.delete_imagem(container, uri)
            return True
        except Exception as exc:
            return False
