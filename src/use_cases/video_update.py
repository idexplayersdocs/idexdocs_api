from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_videos import VideoRepo


class VideoUpdateUseCase:
    def __init__(
        self,
        video_repository: VideoRepo,
    ):
        self.video_repository = video_repository

    def execute(self, http_request: HttpRequest):
        video_data: dict = http_request.json
        video_id: int = video_data.pop('video_id')

        self._check_video_exists(video_id)

        return self._update_image(video_id, video_data)

    def _check_video_exists(self, video_id: int):
        video = self.video_repository.get_video_by_id(video_id)
        if video is None:
            raise NotFoundError('Vídeo não encontrada')

    def _update_image(self, video_id: int, video_data: dict):
        return self.video_repository.update_video(video_id, video_data)
