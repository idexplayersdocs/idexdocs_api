from datetime import datetime

import pytz
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import AtletaImagens


class ArquivoTextRepo:
    def __init__(self, class_model) -> None:
        self.session_factory = create_session
        self.class_model = class_model

    def _create_imagens_list_objects(self, result: list) -> list:
        return [
            {
                'id': imagem.id,
                'blob_url': imagem.blob_url,
                'descricao': imagem.descricao,
            }
            for imagem in result
        ]

    def save_files_uri(self, files_data: dict):
        with self.session_factory() as session:
            file = self.class_model(**files_data)
            session.add(file)
            session.commit()

    def get_file_by_id(self, file_id: int):
        with self.session_factory() as session:
            query = select(self.class_model).where(self.class_model.id == file_id)

        try:
            result = session.exec(query).one()
            return result
        except NoResultFound:
            return None
    #TODO: Implementar o método get_file_by_id para retornar o arquivo com base no ID fornecido.
    def get_file_uris(self, atleta_id: int, filters: dict = {}):
        with self.session_factory() as session:
            query = select(self.class_model).where(
                self.class_model.atleta_id == atleta_id
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

    def update_files(self, file_id: int, file_data: dict):
        with self.session_factory() as session:
            file: self.class_model = session.exec(
                select(self.class_model).where(self.class_model.id == file_id)
            ).one()

            file.descricao = file_data.get('descricao')
            file.data_atualizado = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            )

            session.commit()

    def delete_file(self, file_id: int):
        with self.session_factory() as session:
            file: self.class_model = session.exec(
                select(self.class_model).where(self.class_model.id == file_id)
            ).one()

            session.delete(file)
            session.commit()

            return {'id': file.id}