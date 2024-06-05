import re
import uuid

from fastapi import UploadFile

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_videos import VideoRepo


class VideoUploadUseCase:
    MIME_TYPE_EXT_MAP: dict[str, str] = {
        'video/mp4': '.mp4',
        'video/quicktime': '.mov',
        # Add more video MIME types and their corresponding extensions as needed
    }

    def __init__(
        self,
        atleta_repository: AtletaRepo,
        video_repository: VideoRepo,
        storage_service: AzureBlobStorage,
    ):
        self.atleta_repository = atleta_repository
        self.video_repository = video_repository
        self.storage_service = storage_service

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get('id')
        video_file: UploadFile = http_request.files.get('video')
        video_url: dict = http_request.json

        self._check_atleta_exists(atleta_id)

        if video_file:
            self._upload_video('atleta-videos', video_file, atleta_id)
        elif video_url:
            url = self._parse_video_url(**video_url)
            self._save_video_url_in_database(atleta_id, 'youtube', url)
        else:
            raise ValueError('No video provided')

        return self._format_response()

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _upload_video(
        self, container_name: str, video_file: UploadFile, atleta_id: int
    ):
        mime_type = video_file.content_type
        extension = self.MIME_TYPE_EXT_MAP.get(mime_type)

        if not extension:
            raise RuntimeError(f'Tipo de arquivo não suportado: {mime_type}')

        unique_identifier = uuid.uuid4()
        filename_with_extension = (
            f'atleta_{atleta_id}/{unique_identifier}{extension}'
        )
        file_description = video_file.filename.split('.')[0]

        try:
            file_data = video_file.file.read()
            self.storage_service.upload_image(
                container_name, file_data, filename_with_extension
            )

            blob_url = f'{container_name}/{filename_with_extension}'  # Note: This could be the full URL depending on the implementation of the `upload_blob` method.

            self._save_video_url_in_database(
                atleta_id, 'video', blob_url, file_description
            )
        except Exception as e:
            raise RuntimeError(f'Erro ao salvar o vídeo: {e}')

    def _parse_video_url(self, video_url: str):
        # Regular expressions for extracting the video id
        youtube_standard_url_pattern = r'(?:v=)([a-zA-Z0-9_-]{11})'
        youtube_short_url_pattern = r'(?:youtu.be/)([a-zA-Z0-9_-]{11})'

        # Search for matches in the url
        standard_match = re.search(youtube_standard_url_pattern, video_url)
        short_match = re.search(youtube_short_url_pattern, video_url)

        # Extract the video ID
        if standard_match:
            video_id = standard_match.group(1)
        elif short_match:
            video_id = short_match.group(1)
        else:
            return None  # If no pattern matches

        return f'https://www.youtube.com/embed/{video_id}'

    def _save_video_url_in_database(
        self,
        atleta_id: int,
        tipo_video: str,
        file_name: str,
        file_description: str = None,
    ):
        # Determine the blob url based on the tipo_video
        blob_url = f'{self.storage_service.account_url}/{file_name}' if tipo_video == 'video' else file_name

        # Create the video data dictionary
        video_data = {
            'atleta_id': atleta_id,
            'blob_url': blob_url,
            'tipo': tipo_video,
            'descricao': file_description,
        }

        # Save the video data to the repository
        self.video_repository.save_video_url(video_data)

    def _format_response(self) -> dict:
        return {
            'type': 'VideoUpload',
            'message': 'Vídeo salvo com sucesso',
        }
