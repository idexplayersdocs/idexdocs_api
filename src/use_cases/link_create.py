from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_links import LinkRepo


class LinkCreateUseCase:
    def __init__(self, link_repository: LinkRepo, atleta_repository: AtletaRepo):
        self.link_repository = link_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        link_data: dict = dict(http_request.json)

        atleta_id: int = link_data.get("atleta_id")

        self._check_atleta_exists(atleta_id)

        return self._create_link(link_data)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError("Atleta não encontrado")

    def _create_link(self, link_data: dict):
        link = self.link_repository.create_link(link_data)

        return link
