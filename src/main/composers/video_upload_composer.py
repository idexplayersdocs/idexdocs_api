from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.video_upload_controler import (
    VideoUploadController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_videos import VideoRepo
from src.use_cases.video_upload import VideoUploadUseCase


def video_upload_composer():
    atleta_repository = AtletaRepo()
    video_repository = VideoRepo()
    storage_service = AzureBlobStorage()

    use_case = VideoUploadUseCase(
        atleta_repository=atleta_repository,
        storage_service=storage_service,
        video_repository=video_repository
    )
    controller = VideoUploadController(use_case=use_case)

    return controller.handle
