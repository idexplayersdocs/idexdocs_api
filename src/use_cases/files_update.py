from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_arquivos import ArquivoRepo


class UpdateImagemUseCase:
    def __init__(
        self,
        arquivo_repository: ArquivoRepo,
    ):
        self.arquivo_repository = arquivo_repository

    def execute(self, http_request: HttpRequest):
        imagem_data: dict = http_request.json
        imagem_id: int = imagem_data.pop('imagem_id')

        self._check_imagem_exists(imagem_id)

        return self._update_image(imagem_id, imagem_data)

    def _update_image(self, imagem_id: int, imagem_data: dict):
        return self.arquivo_repository.update_imagem(imagem_id, imagem_data)

    def _check_imagem_exists(self, imagem_id: int):
        blob = self.arquivo_repository.get_imagem_by_id(imagem_id)

        if blob is None:
            raise NotFoundError('Imagem não encontrada')