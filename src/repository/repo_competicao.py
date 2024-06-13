from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select, update

from src.repository.model_objects import HistoricoCompeticao, datetime_now_sec

from .base_repo import create_session


class CompeticaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_competicao_object(self, result: list) -> list[dict]:
        competicao_list = [
            {
                'competicao_id': id_,
                'nome': nome,
                'data_competicao': data_competicao.strftime('%Y-%m-%d'),
                'jogos_completos': jogos_completos,
                'jogos_parciais': jogos_parciais,
                'minutagem': minutagem,
                'gols': gols,
                'assistencias': assistencias,
            }
            for id_, nome, data_competicao, jogos_completos, jogos_parciais, minutagem, gols, assistencias in result
        ]

        return competicao_list

    def list_competicao(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                HistoricoCompeticao.id,
                HistoricoCompeticao.nome,
                HistoricoCompeticao.data_competicao,
                HistoricoCompeticao.jogos_completos,
                HistoricoCompeticao.jogos_parciais,
                HistoricoCompeticao.minutagem,
                HistoricoCompeticao.gols,
                HistoricoCompeticao.assistencias,
            ).where(HistoricoCompeticao.atleta_id == atleta_id)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(HistoricoCompeticao.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_competicao_object(
                paginated_results
            )

    def create_competicao(self, competicao_data: dict) -> dict:
        with self.session_factory() as session:
            new_competicao = HistoricoCompeticao(**competicao_data)
            session.add(new_competicao)
            session.commit()
            session.refresh(new_competicao)
            return {'id': new_competicao.id}

    def update_competicao(self, competicao_data: dict) -> dict:
        competicao_data.update({'data_atualizado': datetime_now_sec()})

        with self.session_factory() as session:
            result = session.exec(
                update(HistoricoCompeticao)
                .where(
                    HistoricoCompeticao.id
                    == competicao_data.pop('competicao_id')
                )
                .values(**competicao_data)
            )
            if result.rowcount == 0:
                raise NoResultFound(
                    'Competição não encontrada no histórico com o ID indicado'
                )
            session.commit()
