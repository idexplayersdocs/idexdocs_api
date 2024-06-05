from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_relacionamento import RelacionamentoRepo


class RelacionamentoCreateUseCase:
    def __init__(
        self,
        relacionamento_repository: RelacionamentoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.relacionamento_repository = relacionamento_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        relacionamento_data: dict = dict(http_request.json)

        atleta_id: int = relacionamento_data.get('atleta_id')

        self._check_atleta_exists(atleta_id)

        return self._create_relacionamentos(relacionamento_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _create_relacionamentos(self, relacionamento_data: dict):
        relacionamento = self.relacionamento_repository.create_relacionamento(
            relacionamento_data
        )

        return relacionamento
