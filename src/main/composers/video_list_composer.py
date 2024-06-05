from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.video_list_controler import (
    VideoListController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_videos import VideoRepo
from src.use_cases.video_list import VideoListUseCase


def video_list_composer():
    atleta_repository = AtletaRepo()
    video_repository = VideoRepo()
    storage_service = AzureBlobStorage()

    use_case = VideoListUseCase(
        atleta_repository=atleta_repository,
        storage_service=storage_service,
        video_repository=video_repository
    )
    controller = VideoListController(use_case=use_case)

    return controller.handle
