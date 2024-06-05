from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import Relacionamento


class RelacionamentoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_relacionamento_list_objects(self, result: list) -> dict:
        return [
            {
                'atleta_id': atleta_id,
                'receptividade_contrato': receptividade_contrato,
                'satisfacao_empresa': satisfacao_empresa,
                'satisfacao_clube': satisfacao_clube,
                'relacao_familiares': relacao_familiares,
                'influencias_externas': influencias_externas,
                'pendencia_empresa': pendencia_empresa,
                'pendencia_clube': pendencia_clube,
                'data_avaliacao': data_avaliacao.strftime('%Y-%m-%d'),
            }
            for atleta_id, receptividade_contrato, satisfacao_empresa, satisfacao_clube, relacao_familiares, influencias_externas, pendencia_empresa, pendencia_clube, data_avaliacao in result
        ]

    def list_relacionamento(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                Relacionamento.atleta_id,
                Relacionamento.receptividade_contrato,
                Relacionamento.relacao_familiares,
                Relacionamento.satisfacao_empresa,
                Relacionamento.satisfacao_clube,
                Relacionamento.influencias_externas,
                Relacionamento.pendencia_clube,
                Relacionamento.pendencia_empresa,
                Relacionamento.data_avaliacao,
            ).filter(Relacionamento.atleta_id == atleta_id)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Relacionamento.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_relacionamento_list_objects(
                paginated_results
            )

    def create_relacionamento(self, relacionamento_data: dict) -> dict:
        with self.session_factory() as session:
            new_relacionamento = Relacionamento(**relacionamento_data)
            session.add(new_relacionamento)
            session.commit()
            session.refresh(new_relacionamento)
            return {'id': new_relacionamento.id}
