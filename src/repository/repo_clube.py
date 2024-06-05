from datetime import datetime

from sqlmodel import func, select

from src.repository.model_objects import HistoricoClube

from .base_repo import create_session


class ClubeRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_clube_objects(self, result: list) -> list[dict]:
        clube_list = [
            {
                'clube_id': id_,
                'nome': nome,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d')
                if data_fim is not None
                else None,
            }
            for id_, nome, data_inicio, data_fim in result
        ]

        return clube_list

    def list_clube(self, atleta_id: int, filters: dict = {}):
        with self.session_factory() as session:
            query = select(
                HistoricoClube.id,
                HistoricoClube.nome,
                HistoricoClube.data_inicio,
                HistoricoClube.data_fim,
            ).where(HistoricoClube.atleta_id == atleta_id)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(HistoricoClube.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_clube_objects(paginated_results)

    def create_clube(self, clube_data: dict) -> dict:
        with self.session_factory() as session:
            new_clube = HistoricoClube(**clube_data)
            session.add(new_clube)
            session.commit()
            session.refresh(new_clube)
            return {'id': new_clube.id}

    def update_data_fim(self, historico_clube_id: int, new_data_fim: str):
        with self.session_factory() as session:
            statement = select(HistoricoClube).where(
                HistoricoClube.id == historico_clube_id
            )
            clube = session.exec(statement).one()

            clube.data_fim = new_data_fim
            clube.data_atualizado = datetime.now()
            session.add(clube)
            session.commit()
            session.refresh(clube)
