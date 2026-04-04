from fastapi import UploadFile

from src.error.types.contrato_existente import ContratoExistente
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.model_objects import Contrato
from src.repository.repo_contrato import ContratoRepo


class ContratoUpdateUseCase:
    MIME_TYPE_EXT_MAP: dict[str, str] = {
        'image/jpeg': '.jpeg',
        'image/png': '.png',
        'image/jpg': '.jpg',
        'application/pdf': '.pdf',
    }

    def __init__(
        self,
        contrato_repository: ContratoRepo,
        storage_service: AzureBlobStorage = None,
    ):
        self.contrato_repository = contrato_repository
        self.storage_service = storage_service

    def execute(self, http_request: HttpRequest):
        if http_request.json:
            contrato_data = dict(http_request.json)
            file = None
        else:
            form = http_request.files
            contrato_data = {
                'contrato_id': int(form.get('contrato_id')),
                'data_inicio': form.get('data_inicio'),
                'data_termino': form.get('data_termino'),
                'observacao': form.get('observacao') or None,
                'ativo': form.get('ativo', 'true').lower() in ('true', '1', 'yes'),
            }
            file = form.get('arquivo')

        result = self._update_contrato(contrato_data)

        # Upload file if provided
        contrato_id = contrato_data.get('contrato_id')
        if file and self.storage_service and contrato_id:
            arquivo_url = self._upload_file('atleta-contratos', file, contrato_id)
            self.contrato_repository.update_contrato_arquivo_url(contrato_id, arquivo_url)

        return result

    def _update_contrato(self, contrato_data: dict):
        contrato = self.contrato_repository.update_contrato(contrato_data)
        return contrato

    def _upload_file(self, container_name: str, file: UploadFile, contrato_id: int) -> str:
        mime_type = file.content_type
        extension = self.MIME_TYPE_EXT_MAP.get(mime_type)

        if not extension:
            raise RuntimeError(f'Tipo de arquivo não suportado: {mime_type}')

        filename = f'contrato_{contrato_id}{extension}'

        try:
            file_data = file.file.read()
            self.storage_service.upload_image(container_name, file_data, filename)

            account_url = self.storage_service.account_url
            blob_url = f'{account_url}/{container_name}/{filename}'
            return blob_url
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar o arquivo do contrato: {e}')
