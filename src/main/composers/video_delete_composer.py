from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.video_delete_controler import (
    VideoDeleteController,
)
from src.repository.repo_videos import VideoRepo
from src.use_cases.video_delete import VideoDeleteUseCase


def video_delete_composer():
    video_repository = VideoRepo()
    storage_service = AzureBlobStorage()

    use_case = VideoDeleteUseCase(
        storage_service=storage_service,
        video_repository=video_repository
    )
    controller = VideoDeleteController(use_case=use_case)

    return controller.handle
