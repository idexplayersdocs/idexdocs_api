from datetime import datetime

import pytz
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import AtletaImagens


class ArquivoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_imagens_list_objects(self, result: list) -> list:
        return [
            {
                'id': imagem.id,
                'blob_url': imagem.blob_url,
                'descricao': imagem.descricao,
            }
            for imagem in result
        ]

    def save_imagens_url(self, imagem_data: dict):
        with self.session_factory() as session:
            atleta_imagem = AtletaImagens(**imagem_data)
            session.add(atleta_imagem)
            session.commit()

    def get_imagem_by_id(self, imagem_id: int):
        with self.session_factory() as session:
            query = select(AtletaImagens).where(AtletaImagens.id == imagem_id)

        try:
            result = session.exec(query).one()
            return result
        except NoResultFound:
            return None

    def get_imagens_urls(self, atleta_id: int, filters: dict = {}):
        with self.session_factory() as session:
            query = select(AtletaImagens).where(
                AtletaImagens.atleta_id == atleta_id
            )

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(AtletaImagens.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_imagens_list_objects(
                paginated_results
            )

    def update_imagem(self, imagem_id: int, imagem_data: dict):
        with self.session_factory() as session:
            imagem: AtletaImagens = session.exec(
                select(AtletaImagens).where(AtletaImagens.id == imagem_id)
            ).one()

            imagem.descricao = imagem_data.get('descricao')
            imagem.data_atualizado = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            )

            session.commit()

    def delete_imagem(self, imagem_id: int):
        with self.session_factory() as session:
            imagem: AtletaImagens = session.exec(
                select(AtletaImagens).where(AtletaImagens.id == imagem_id)
            ).one()

            session.delete(imagem)
            session.commit()

            return {'id': imagem.id}
