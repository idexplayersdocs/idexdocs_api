from src.presentation.controllers.files_update_controler import (
    ImagemUpdateController,
)
from src.repository.repo_arquivos import ArquivoRepo
from src.use_cases.files_update import UpdateImagemUseCase


def update_files_composer():
    arquivo_repository = ArquivoRepo()

    use_case = UpdateImagemUseCase(
        arquivo_repository=arquivo_repository,
    )
    controller = ImagemUpdateController(use_case=use_case)

    return controller.handle
