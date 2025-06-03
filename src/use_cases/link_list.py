from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_links import LinkRepo


class LinkListUseCase:
    def __init__(self, link_repository: LinkRepo):
        self.link_repository = link_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        total_count, result = self._list_link(atleta_id, filters)
        return self._format_response(total_count, result)

    def _list_link(self, atleta_id: int, filters: dict):
        links = self.link_repository.get_links(atleta_id, filters)

        if len(links) == 0:
            raise NotFoundError('O Atleta não possui links cadastrados')

        return links

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Links',
            'data': result,
        }
