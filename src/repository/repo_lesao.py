from sqlmodel import func, select

from src.repository.model_objects import HistoricoLesao

from .base_repo import create_session


class LesaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_lesao_objects(self, result: list) -> list[dict]:
        lesao_list = [
            {
                'data_lesao': data_lesao.strftime('%Y-%m-%d'),
                'descricao': descricao,
                'data_retorno': data_retorno.strftime('%Y-%m-%d'),
            }
            for data_lesao, descricao, data_retorno in result
        ]

        return lesao_list

    def list_lesao(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                HistoricoLesao.data_lesao,
                HistoricoLesao.descricao,
                HistoricoLesao.data_retorno,
            ).where(HistoricoLesao.atleta_id == atleta_id)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(HistoricoLesao.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_lesao_objects(paginated_results)

    def create_lesao(self, lesao_data: dict) -> dict:
        with self.session_factory() as session:
            new_lesao = HistoricoLesao(**lesao_data)
            session.add(new_lesao)
            session.commit()
            session.refresh(new_lesao)
            return {'id': new_lesao.id}
