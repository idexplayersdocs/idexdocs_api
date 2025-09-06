from abc import ABC, abstractmethod
from typing import override

from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class FileDownloadInterface(ABC):
    def __init__(self, atleta_repository: AtletaRepo, tipo: str) -> None:
        self.atleta_repository = atleta_repository

    @abstractmethod
    def download(self, http_request: HttpRequest) -> dict:
        pass

    def _get_blob_uri(self, _id: int, tipo: str) -> None:
        return self.atleta_repository.get_blob_url(_id, tipo)

    def _format_response(
        self, blob_url: str | None
    ) -> dict[str, bool | str | None]:
        return {'status': bool(blob_url), 'blob_url': blob_url}


class FileDownload(FileDownloadInterface):
    def __init__(self, atleta_repository: AtletaRepo, tipo: str) -> None:
        super().__init__(atleta_repository, tipo)
        self.tipo = tipo

    @override
    def download(self, http_request: HttpRequest) -> dict:
        _id: int = http_request.path_params.get('id')

        uri: str | None = self._get_blob_uri(_id, self.tipo)

        return self._format_response(uri)


class FileDownloadUseCase:
    def __init__(self, atleta_repository: AtletaRepo) -> None:
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest) -> dict:
        strategy: FileDownloadInterface = self._pick_strategy(http_request)
        return strategy.download(http_request)

    def _pick_strategy(
        self, http_request: HttpRequest
    ) -> FileDownloadInterface:
        url = http_request.url.path.lower()

        if 'atleta' in url:
            return FileDownload(
                tipo='atleta', atleta_repository=self.atleta_repository
            )
        elif 'recibo' in url:
            return FileDownload(
                tipo='recibo', atleta_repository=self.atleta_repository
            )
        elif 'contrato' in url:
            return FileDownload(
                tipo='contrato', atleta_repository=self.atleta_repository
            )
        else:
            raise NotImplementedError(
                'Estratégia de download não implementada para este tipo de arquivo'
            )
