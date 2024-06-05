from sqlmodel import desc, select

from .base_repo import create_session
from .model_objects import HistoricoObservacao


class ObservacaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_observacao_get_objects(self, result: list) -> dict:
        if not result:
            return None
        return {
            'id': result.id,
            'tipo': result.tipo.value,
            'descricao': result.descricao,
            'data_criacao': result.data_criacao.strftime('%Y-%m-%d'),
        }

    def list_observacao(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = (
                select(
                    HistoricoObservacao.id,
                    HistoricoObservacao.tipo,
                    HistoricoObservacao.descricao,
                    HistoricoObservacao.data_criacao,
                )
                .filter(HistoricoObservacao.atleta_id == atleta_id)
                .order_by(desc(HistoricoObservacao.data_criacao))
            )

            if tipo := filters.get('tipo'):
                query = query.filter(HistoricoObservacao.tipo == tipo)

            return self._create_observacao_get_objects(
                session.exec(query).first()
            )

    def create_observacao(self, observacao_data: dict) -> dict:
        with self.session_factory() as session:
            new_observacao = HistoricoObservacao(**observacao_data)
            session.add(new_observacao)
            session.commit()
            session.refresh(new_observacao)
            return {'id': new_observacao.id}
