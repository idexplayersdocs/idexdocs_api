from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_arquivos import ArquivoRepo
from src.repository.repo_atleta import AtletaRepo


class MultipleFilesDownloadUseCase:
    def __init__(
        self, atleta_repository: AtletaRepo, arquivo_repository: ArquivoRepo
    ):
        self.atleta_repository = atleta_repository
        self.arquivo_repository = arquivo_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)
        total_count, blob_urls = self._get_blob_url(atleta_id, filters)

        return self._format_response(total_count, blob_urls)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _get_blob_url(self, atleta_id: int, filters: dict):
        return self.arquivo_repository.get_imagens_urls(atleta_id, filters)

    def _format_response(self, total_count: int, result: list[dict]):
        return {
            'count': len(result),
            'total': total_count,
            'type': 'AtletaImagens',
            'data': result,
        }
