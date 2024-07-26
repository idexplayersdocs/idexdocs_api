from sqlalchemy.exc import NoResultFound
from sqlmodel import func, select, update

from src.repository.model_objects import HistoricoClube, datetime_now_sec


class ClubeRepo:
    def __init__(self, session) -> None:
        self.session_factory = session

    def _create_clube_objects(self, result: list) -> list[dict]:
        clube_list = [
            {
                'clube_id': id_,
                'nome': nome,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d')
                if data_fim is not None
                else None,
                'clube_atual': clube_atual,
            }
            for id_, nome, data_inicio, data_fim, clube_atual in result
        ]

        return clube_list

    def list_clube(self, atleta_id: int, filters: dict = {}):
        with self.session_factory as session:
            query = select(
                HistoricoClube.id,
                HistoricoClube.nome,
                HistoricoClube.data_inicio,
                HistoricoClube.data_fim,
                HistoricoClube.clube_atual,
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
        with self.session_factory as session:
            new_clube = HistoricoClube(**clube_data)
            session.add(new_clube)
            session.commit()
            session.refresh(new_clube)
            return {'id': new_clube.id}

    def update_clube(self, clube_data: dict):
        clube_data.update({'data_atualizado': datetime_now_sec()})

        with self.session_factory() as session:
            result = session.exec(
                update(HistoricoClube)
                .where(HistoricoClube.id == clube_data.pop('clube_id'))
                .values(**clube_data)
            )

            if result.rowcount == 0:
                raise NoResultFound(
                    'Clube não encontrado no histórico com o ID indicado'
                )

            session.commit()
