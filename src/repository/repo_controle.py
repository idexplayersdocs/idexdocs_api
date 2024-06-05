from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import HistoricoControle


class ControleRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_controle_list_objects(self, result: list) -> dict:
        return [
            {
                'atleta_id': atleta_id,
                'nome': nome,
                'quantidade': quantidade,
                'preco': preco,
                'data_controle': data_controle.strftime('%Y-%m-%d'),
            }
            for atleta_id, nome, quantidade, preco, data_controle in result
        ]

    def list_controle(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                HistoricoControle.id,
                HistoricoControle.nome,
                HistoricoControle.quantidade,
                HistoricoControle.preco,
                HistoricoControle.data_controle,
            ).filter(HistoricoControle.atleta_id == atleta_id)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(HistoricoControle.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_controle_list_objects(
                paginated_results
            )

    def create_controle(self, controle_data: dict) -> dict:
        with self.session_factory() as session:
            new_controle = HistoricoControle(**controle_data)
            session.add(new_controle)
            session.commit()
            session.refresh(new_controle)
            return {'id': new_controle.id}
