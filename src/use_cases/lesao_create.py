from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_lesao import LesaoRepo


class LesaoCreateUseCase:
    def __init__(
        self,
        lesao_repository: LesaoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.lesao_repository = lesao_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        lesao_data: dict = dict(http_request.json)

        atleta_id: int = lesao_data.get('atleta_id')

        self._check_atleta_exists(atleta_id)

        return self._create_lesao(lesao_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _create_lesao(self, lesao_data: dict):
        lesao = self.lesao_repository.create_lesao(lesao_data)

        return lesao
