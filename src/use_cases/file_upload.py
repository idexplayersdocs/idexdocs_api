from fastapi import UploadFile

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class FileUploadUseCase:
    MIME_TYPE_EXT_MAP: dict[str, str] = {
        'image/jpeg': '.jpeg',
        'image/png': '.png',
        # Add more MIME types and their corresponding extensions as needed
    }

    def __init__(
        self, atleta_repository: AtletaRepo, storage_service: AzureBlobStorage
    ):
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get('id')
        image_file: UploadFile = http_request.files.get('image')

        self._check_atleta_exists(atleta_id)
        self._upload_image('atleta-avatar', image_file, atleta_id)

        return self._format_response()

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _upload_image(
        self, container_name: str, image_file: UploadFile, atleta_id: int
    ):
        mime_type = image_file.content_type
        extension = self.MIME_TYPE_EXT_MAP.get(mime_type)

        if not extension:
            raise RuntimeError(f'Tipo de arquivo não suportado: {mime_type}')

        filename_with_extension = f'atleta_{atleta_id}{extension}'

        try:
            file_data = image_file.file.read()
            self.storage_service.upload_image(
                container_name, file_data, filename_with_extension
            )

            blob_url = f'{container_name}/{filename_with_extension}'

            self._save_blob_url_in_database(atleta_id, blob_url)
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar a imagem: {e}')

    def _save_blob_url_in_database(self, atleta_id: int, file_name: str):
        account_url = self.storage_service.account_url
        blob_url = account_url + '/' + file_name
        self.atleta_repository.save_blob_url(atleta_id, blob_url)

    def _format_response(self) -> dict:
        return {
            'type': 'FileUpload',
            'status': True,
            'message': 'Arquivo salvo com sucesso',
        }
