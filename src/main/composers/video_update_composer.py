from src.presentation.controllers.video_update_controler import (
    VideoUpdateController,
)
from src.repository.repo_videos import VideoRepo
from src.use_cases.video_update import VideoUpdateUseCase


def video_update_composer():
    video_repository = VideoRepo()

    use_case = VideoUpdateUseCase(
        video_repository=video_repository
    )
    controller = VideoUpdateController(use_case=use_case)

    return controller.handle
