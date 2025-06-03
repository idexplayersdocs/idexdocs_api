from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_links import LinkRepo


class LinkDeleteUseCase:
    def __init__(
        self,
        link_repository: LinkRepo,
    ):
        self.link_repository = link_repository

    def execute(self, http_request: HttpRequest):
        link_id: int = http_request.path_params.get("id")

        return self._delete_link(link_id)

    def _delete_link(self, link_id: int):
        link = self.link_repository.delete_link(link_id)

        return link
