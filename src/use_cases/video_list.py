from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_videos import VideoRepo


class VideoListUseCase:
    def __init__(
        self,
        atleta_repository: AtletaRepo,
        storage_service: AzureBlobStorage,
        video_repository: VideoRepo,
    ):
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository
        self.video_repository = video_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get('id')

        self._check_atleta_exists(atleta_id)
        total_count, blob_urls = self._get_blob_url(atleta_id)

        return self._format_response(total_count, blob_urls)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _get_blob_url(self, atleta_id: int):
        return self.video_repository.get_videos_urls(atleta_id)

    def _format_response(self, total_count: int, result: list[dict]):
        return {
            'count': len(result),
            'total': total_count,
            'type': 'AtletaVideos',
            'data': result,
        }
