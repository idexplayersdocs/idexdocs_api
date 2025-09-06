"""This module aims to handle file uploads from different endpoints.

An interface is implemented "FileUploadStrategy" to expose common methods for
new implementations.

The term "parent" is used to convey the dependency between the file being uploaded
and it's owner of the object. For example:

(Parent) -> (Child)

Athelete -> image  (file),
Contract -> image  (file),
Receipt  -> image  (file),
...
"""

from abc import ABC, abstractmethod
from typing import override

from fastapi import UploadFile

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_contrato import ContratoRepo
from src.repository.repo_controle import ControleRepo


class FileUploadStrategy(ABC):
    """Strategy interface"""

    MIME_TYPE_EXT_MAP: dict[str | None, str] = {
        'image/jpeg': '.jpeg',
        'image/png': '.png',
        'application/pdf': '.pdf',
    }

    def __init__(
        self, storage_service: AzureBlobStorage, atleta_repository: AtletaRepo
    ) -> None:
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository

    @abstractmethod
    def upload(self, http_request: HttpRequest) -> dict:
        pass

    @abstractmethod
    def _check_parent_exists(self, parent_id: int) -> None:
        pass

    def _save_blob_uri_in_database(
        self, object_id: int, file_name: str, tipo: str
    ) -> None:
        account_url = self.storage_service.account_url
        uri = account_url + file_name
        self.atleta_repository.save_blob_url(object_id, uri, tipo)

    def _upload_file(
        self, container_name: str, file: UploadFile, object_id: int, tipo: str
    ) -> None:

        mime_type: str | None = file.content_type
        extension: str | None = self.MIME_TYPE_EXT_MAP.get(mime_type)

        if not extension:
            raise RuntimeError(f'Tipo de arquivo não suportado: {mime_type}')

        object_name: str = container_name.split('-')[1]

        filename_with_extension = f'{object_name}_{object_id}{extension}'

        try:
            file_data: bytes = file.file.read()
            self.storage_service.upload_image(
                container_name, file_data, filename_with_extension
            )
            uri: str = f'{container_name}/{filename_with_extension}'

            self._save_blob_uri_in_database(object_id, uri, tipo)
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar a arquivo: {e}')

    def _format_response(self) -> dict:
        return {
            'type': 'FileUpload',
            'status': True,
            'message': 'Arquivo salvo com sucesso',
        }


class AtheteAvatarUploadStrategy(FileUploadStrategy):
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        parent_repository: AtletaRepo,
        tipo: str,
    ) -> None:
        super().__init__(storage_service, parent_repository)
        self.parent_repository = parent_repository
        self.tipo = tipo

    @override
    def upload(self, http_request: HttpRequest) -> dict:
        _id: int = http_request.path_params.get('id')
        file: UploadFile = http_request.files.get('image')

        self._check_parent_exists(_id)
        self._upload_file('atleta-avatar', file, _id, self.tipo)

        return self._format_response()

    @override
    def _check_parent_exists(self, parent_id: int) -> None:
        atleta = self.parent_repository.get_atleta_by_id(parent_id)
        if atleta is None:
            raise NotFoundError('Objeto de referência não encontrado')


class ReceiptUploadStrategy(FileUploadStrategy):
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        parent_repository: ControleRepo,
        atleta_repository: AtletaRepo,
        tipo: str,
    ) -> None:
        super().__init__(storage_service, atleta_repository)
        self.parent_repository = parent_repository
        self.tipo = tipo

    @override
    def upload(self, http_request: HttpRequest) -> dict:
        _id: int = http_request.path_params.get('id')
        file: UploadFile = http_request.files.get('arquivo')

        self._check_parent_exists(_id)
        self._upload_file('atleta-controles', file, _id, self.tipo)

        return self._format_response()

    @override
    def _check_parent_exists(self, parent_id: int) -> None:
        parent = self.parent_repository.get_by_id(parent_id)
        if parent is None:
            raise NotFoundError('Objeto de referência não encontrado')


class ContratoUploadStrategy(FileUploadStrategy):
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        parent_repository: ContratoRepo,
        atleta_repository: AtletaRepo,
        tipo: str,
    ) -> None:
        super().__init__(storage_service, atleta_repository)
        self.parent_repository = parent_repository
        self.tipo = tipo

    @override
    def upload(self, http_request: HttpRequest) -> dict:
        _id: int = http_request.path_params.get('id')
        file: UploadFile = http_request.files.get('file')

        self._check_parent_exists(_id)
        self._upload_file('atleta-contratos', file, _id, self.tipo)

        return self._format_response()

    @override
    def _check_parent_exists(self, parent_id: int) -> None:
        parent = self.parent_repository.get_by_id(parent_id)
        if parent is None:
            raise NotFoundError('Objeto de referência não encontrado')


class FileUploadUseCase:
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        atleta_repository: AtletaRepo,
        controle_repository: ControleRepo,
        contrato_repository: ContratoRepo,
    ) -> None:
        self.atleta_repository = atleta_repository
        self.storage_service = storage_service
        self.controle_repository = controle_repository
        self.contrato_repository = contrato_repository

    def execute(self, http_request: HttpRequest) -> dict:
        strategy: FileUploadStrategy = self._pick_strategy(http_request)
        return strategy.upload(http_request)

    def _pick_strategy(self, http_request: HttpRequest) -> FileUploadStrategy:
        url = http_request.url.path.lower()

        if 'atleta' in url:
            return AtheteAvatarUploadStrategy(
                storage_service=self.storage_service,
                parent_repository=self.atleta_repository,
                tipo='atleta',
            )
        elif 'controle' in url:
            return ReceiptUploadStrategy(
                storage_service=self.storage_service,
                parent_repository=self.controle_repository,
                atleta_repository=self.atleta_repository,
                tipo='recibo',
            )
        elif 'contrato' in url:
            return ContratoUploadStrategy(
                storage_service=self.storage_service,
                parent_repository=self.contrato_repository,
                atleta_repository=self.atleta_repository,
                tipo='contrato',
            )
        else:
            raise NotImplementedError(
                'Estratégia de upload não implementada para este tipo de arquivo'
            )
