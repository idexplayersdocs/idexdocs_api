from datetime import datetime

import pytz
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import AtletaVideos


class VideoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_videos_list_objects(self, result: list) -> list:
        return [
            {
                'id': video.id,
                'blob_url': video.blob_url,
                'tipo': video.tipo.value,
                'descricao': video.descricao,
            }
            for video in result
        ]

    def save_video_url(self, video_data: dict):
        with self.session_factory() as session:
            atleta_video = AtletaVideos(**video_data)
            session.add(atleta_video)
            session.commit()

    def get_video_by_id(self, video_id: int):
        with self.session_factory() as session:
            query = select(AtletaVideos).where(AtletaVideos.id == video_id)

        try:
            result = session.exec(query).one()
            return result
        except NoResultFound:
            return None

    def get_videos_urls(self, atleta_id: int, filters: dict = {}):
        with self.session_factory() as session:
            query = select(AtletaVideos).where(
                AtletaVideos.atleta_id == atleta_id
            )

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(AtletaVideos.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_videos_list_objects(
                paginated_results
            )

    def update_video(self, video_id: int, video_data: dict):
        with self.session_factory() as session:
            video: AtletaVideos = session.exec(
                select(AtletaVideos).where(AtletaVideos.id == video_id)
            ).one()

            video.descricao = video_data.get('descricao')
            video.data_atualizado = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            )

            session.commit()

    def delete_video(self, video_id: int):
        with self.session_factory() as session:
            video: AtletaVideos = session.exec(
                select(AtletaVideos).where(AtletaVideos.id == video_id)
            ).one()

            session.delete(video)
            session.commit()

            return {'id': video.id}
