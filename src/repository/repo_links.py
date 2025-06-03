from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import AtletaLink


class LinkRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_links_list_objects(self, result: list) -> list:
        return [
            {"id": link.id, "url": link.url, "descricao": link.descricao}
            for link in result
        ]

    def create_link(self, link_data: dict):
        with self.session_factory() as session:
            atleta_link = AtletaLink(**link_data)
            session.add(atleta_link)
            session.commit()

    def get_links(self, atleta_id: int, filters: dict = {}):
        with self.session_factory() as session:
            query = select(AtletaLink).where(AtletaLink.atleta_id == atleta_id)

        # conta o número total de items sem paginação
        total_count = session.exec(
            select(func.count()).select_from(query.subquery())
        ).one()

        # aplica paginação
        page = int(filters.get("page", 1))
        per_page = int(filters.get("per_page", 10))
        query = (
            query.order_by(AtletaLink.data_criacao)
            .limit(per_page)
            .offset((page - 1) * per_page)
        )

        # executa query com paginação
        paginated_results = session.exec(query).all()

        return total_count, self._create_links_list_objects(paginated_results)

    def delete_link(self, link_id: int):
        with self.session_factory() as session:
            link: AtletaLink = session.exec(
                select(AtletaLink).where(AtletaLink.id == link_id)
            ).one()

            session.delete(link)
            session.commit()

            return {'id': link.id}
