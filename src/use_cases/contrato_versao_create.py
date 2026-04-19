from fastapi import UploadFile

from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_contrato import ContratoRepo

MIME_TYPE_EXT_MAP: dict[str, str] = {
    'application/pdf': '.pdf',
    'image/jpeg': '.jpeg',
    'image/jpg': '.jpg',
    'image/png': '.png',
}

CONTAINER_NAME = 'atleta-contratos'


class ContratoVersaoCreateUseCase:
    def __init__(
        self,
        contrato_repository: ContratoRepo,
        storage_service: AzureBlobStorage | None = None,
    ):
        self.contrato_repository = contrato_repository
        self.storage_service = storage_service

    def execute(self, http_request: HttpRequest) -> dict:
        if http_request.json:
            data = dict(http_request.json)
            arquivo: UploadFile | None = None
        else:
            form = http_request.files
            data = {
                'contrato_id': int(form.get('contrato_id')),
                'data_inicio': form.get('data_inicio'),
                'data_termino': form.get('data_termino'),
                'observacao': form.get('observacao') or None,
            }
            arquivo = form.get('arquivo') or None

        result = self.contrato_repository.create_contrato_versao(
            contrato_id=data['contrato_id'],
            data_inicio=data['data_inicio'],
            data_termino=data['data_termino'],
            observacao=data.get('observacao'),
        )

        versao_id: int = result['id']

        if arquivo and self.storage_service:
            self._upload_file(arquivo, versao_id)

        return result

    def _upload_file(self, arquivo: UploadFile, versao_id: int) -> None:
        mime_type: str | None = arquivo.content_type
        extension: str | None = MIME_TYPE_EXT_MAP.get(mime_type)

        if not extension:
            raise RuntimeError(f'Tipo de arquivo não suportado: {mime_type}')

        filename = f'contrato_versao_{versao_id}{extension}'

        try:
            file_data: bytes = arquivo.file.read()
            self.storage_service.upload_image(CONTAINER_NAME, file_data, filename)
            url: str = f'{self.storage_service.account_url}/{CONTAINER_NAME}/{filename}'
            self.contrato_repository.update_contrato_versao_arquivo_url(versao_id, url)
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar o arquivo: {e}')
