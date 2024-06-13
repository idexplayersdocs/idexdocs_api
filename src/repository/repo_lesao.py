from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select, update

from src.repository.model_objects import HistoricoLesao, datetime_now_sec

from .base_repo import create_session


class LesaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_lesao_objects(self, result: list) -> list[dict]:
        lesao_list = [
            {
                'lesao_id': id_,
                'data_lesao': data_lesao.strftime('%Y-%m-%d'),
                'descricao': descricao,
                'data_retorno': data_retorno.strftime('%Y-%m-%d'),
            }
            for id_, descricao, data_lesao, data_retorno in result
        ]

        return lesao_list

    def list_lesao(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                HistoricoLesao.id,
                HistoricoLesao.descricao,
                HistoricoLesao.data_lesao,
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

    def update_lesao(self, lesao_data: dict) -> dict:
        with self.session_factory() as session:
            result = session.exec(
                update(HistoricoLesao)
                .where(HistoricoLesao.id == lesao_data['lesao_id'])
                .values(
                    data_lesao=lesao_data['data_lesao'],
                    descricao=lesao_data['descricao'],
                    data_retorno=lesao_data['data_retorno'],
                    data_atualizado=datetime_now_sec(),
                )
            )
            if result.rowcount == 0:
                raise NoResultFound(
                    'Lesão não encontrada no histórico com o ID indicado'
                )
            session.commit()
