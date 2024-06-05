from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_observacao import ObservacaoRepo


class ObservacaoCreateUseCase:
    def __init__(
        self,
        observacao_repository: ObservacaoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.observacao_repository = observacao_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        observacao_data: dict = dict(http_request.json)

        atleta_id: int = observacao_data.get('atleta_id')

        self._check_atleta_exists(atleta_id)

        return self._create_observacao(observacao_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _create_observacao(self, observacao_data: dict):
        observacao = self.observacao_repository.create_observacao(
            observacao_data
        )

        return observacao
