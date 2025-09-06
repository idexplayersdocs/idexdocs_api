import os

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient


class AzureBlobStorage:
    # Use a class attribute for the BlobServiceClient if all instances share the same service client config
    _blob_service_client: BlobServiceClient | None = None
    account_url: str | None = os.getenv('STORAGE_ACCOUNT')

    def __init__(self) -> None:

        if not AzureBlobStorage.account_url:
            raise ValueError(
                'STORAGE_ACCOUNT environment variable must be set and non-empty.'
            )

        # Initialize the BlobServiceClient once
        if AzureBlobStorage._blob_service_client is None:
            default_credential = DefaultAzureCredential(
                exclude_environment_credential=True
            )
            AzureBlobStorage._blob_service_client = BlobServiceClient(
                AzureBlobStorage.account_url, credential=default_credential
            )

    def upload_image(
        self, container: str, image_data: bytes, filename: str
    ) -> None:
        container_client: ContainerClient = (
            self._blob_service_client.get_container_client(container)
        )
        if not container_client.exists():
            raise RuntimeError(f"Container '{container}' não existe.")

        try:
            # Get a blob client to perform the upload
            blob_client: BlobClient = (
                self._blob_service_client.get_blob_client(
                    container=container, blob=filename
                )
            )
            blob_client.upload_blob(image_data, overwrite=True)
        except Exception:
            raise

    def get_image_url(self, blob_name: str) -> bytes | None:
        try:
            # Get a blob client to perform the download
            blob_client: BlobClient = (
                self._blob_service_client.get_blob_client(
                    container=self.container_name, blob=blob_name
                )
            )
            # Verificando a existência do blob
            blob_client.get_blob_properties()

            return blob_client.url
        except ResourceNotFoundError:
            print(f'O blob nome {blob_name} não existe')
            return None

    def delete_imagem(self, container: str, blob_name: str) -> None:
        try:
            blob_client: BlobClient = (
                self._blob_service_client.get_blob_client(container, blob_name)
            )

            blob_client.delete_blob()
        except Exception:
            raise
