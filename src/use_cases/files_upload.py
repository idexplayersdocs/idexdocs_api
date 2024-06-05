import uuid

from fastapi import UploadFile

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_arquivos import ArquivoRepo
from src.repository.repo_atleta import AtletaRepo


class MultipleFilesUploadUseCase:
    MIME_TYPE_EXT_MAP: dict[str, str] = {
        'image/jpeg': '.jpeg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        # Add more MIME types and their corresponding extensions as needed
    }

    def __init__(
        self,
        atleta_repository: AtletaRepo,
        storage_service: AzureBlobStorage,
        arquivo_repository: ArquivoRepo,
    ):
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository
        self.arquivo_repository = arquivo_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get('id')
        uploaded_images: list[UploadFile] = http_request.files.getlist('files')

        self._check_atleta_exists(atleta_id)

        for image_file in uploaded_images:
            self._upload_image('atleta-imagens', image_file, atleta_id)

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

        unique_identifier = uuid.uuid4()
        # timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        filename_with_extension = (
            f'atleta_{atleta_id}/{unique_identifier}{extension}'
        )
        file_description = image_file.filename.split('.')[0]

        try:
            file_data = image_file.file.read()
            self.storage_service.upload_image(
                container_name, file_data, filename_with_extension
            )

            blob_url = f'{container_name}/{filename_with_extension}'

            self._save_blob_url_in_database(
                atleta_id, blob_url, file_description
            )
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar a imagem: {e}')

    def _save_blob_url_in_database(
        self, atleta_id: int, file_name: str, file_description: str
    ):
        account_url = self.storage_service.account_url
        blob_url = f'{account_url}/{file_name}'
        imagem_data = {
            'atleta_id': atleta_id,
            'blob_url': blob_url,
            'descricao': file_description,
        }
        self.arquivo_repository.save_imagens_url(imagem_data)

    def _format_response(self) -> dict:
        return {
            'type': 'FilesUpload',
            'status': True,
            'message': 'Arquivo(s) salvo(s) com sucesso',
        }
