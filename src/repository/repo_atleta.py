from collections import namedtuple
from datetime import datetime, timedelta

import pytz
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import (
    Atleta,
    AtletaAvatar,
    Contrato,
    HistoricoClube,
    Posicao,
    Relacionamento,
)

AtletaDetails = namedtuple(
    'AtletaDetails',
    [
        'atleta',
        'data_nascimento',
        'primeira_posicao',
        'segunda_posicao',
        'terceira_posicao',
        'clube_atual',
        'avatar_url',
        'contratos',
    ],
)

ContratoDetails = namedtuple(
    'ContratoDetails',
    [
        'id',
        'data_inicio',
        'data_termino',
        'observacao',
        'versao',
        'ativo',
        'data_criacao',
        'data_atualizado',
        'contrato_sub_tipo_nome',
    ],
)


class AtletaRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_atleta_list_objects(self, result: list) -> dict:
        return [
            {
                'id': id_,
                'nome': nome,
                'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
                'posicao_primaria': primeira.value if primeira else None,
                'clube_atual': clube,
                'data_proxima_avaliacao_relacionamento': (
                    data_avaliacao + timedelta(days=30)
                ).strftime('%Y-%m-%d')
                if data_avaliacao
                else None,
                'ativo': ativo,
            }
            for id_, nome, data_nascimento, primeira, clube, data_avaliacao, ativo in result
        ]

    def _create_atleta_detail_object(self, result: AtletaDetails) -> dict:
        return {
            'nome': result.atleta.nome,
            'data_nascimento': result.atleta.data_nascimento.strftime(
                '%Y-%m-%d'
            ),
            'posicao_primaria': result.primeira_posicao.value
            if result.primeira_posicao
            else None,
            'posicao_secundaria': result.segunda_posicao.value
            if result.segunda_posicao
            else None,
            'posicao_terciaria': result.terceira_posicao.value
            if result.terceira_posicao
            else None,
            'clube_atual': result.clube_atual,
            'contratos': [
                {
                    'tipo': contrato.contrato_sub_tipo_nome,
                    'data_inicio': contrato.data_inicio.strftime('%Y-%m-%d'),
                    'data_termino': contrato.data_termino.strftime('%Y-%m-%d'),
                    'data_expiracao': (
                        contrato.data_termino - timedelta(days=180)
                    ).strftime('%Y-%m-%d'),
                }
                for contrato in result.contratos
            ],
            'blob_url': result.avatar_url,
            'ativo': result.atleta.ativo,
        }

    def list_atleta(self, filters: dict):
        with self.session_factory() as session:
            subquery = (
                select(
                    Relacionamento.atleta_id,
                    func.max(Relacionamento.data_avaliacao).label(
                        'max_data_avaliacao'
                    ),
                )
                .group_by(Relacionamento.atleta_id)
                .subquery()
            )

            query = (
                select(
                    Atleta.id.label('id_'),
                    Atleta.nome.label('nome'),
                    Atleta.data_nascimento.label('data_nascimento'),
                    Posicao.primeira,
                    HistoricoClube.nome.label('clube'),
                    Relacionamento.data_avaliacao,
                    Atleta.ativo,
                )
                .select_from(Atleta)
                .outerjoin(Posicao, Posicao.atleta_id == Atleta.id)
                .outerjoin(
                    HistoricoClube, Atleta.id == HistoricoClube.atleta_id
                )
                .outerjoin(subquery, subquery.c.atleta_id == Atleta.id)
                .outerjoin(
                    Relacionamento,
                    (
                        (Relacionamento.atleta_id == subquery.c.atleta_id)
                        & (
                            Relacionamento.data_avaliacao
                            == subquery.c.max_data_avaliacao
                        )
                    ),
                )
                .where(HistoricoClube.data_fim.is_(None))
                .order_by(Atleta.id)
            )

            if atleta := filters.get('atleta'):
                query = query.filter(Atleta.nome == atleta)

            if posicao := filters.get('posicao'):
                query = query.filter(Posicao.primeira == posicao)

            if clube := filters.get('clube'):
                query = query.filter(HistoricoClube.nome == clube)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Atleta.nome)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_atleta_list_objects(
                paginated_results
            )

    def get_atleta_by_id(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(Atleta).where(Atleta.id == atleta_id)

        try:
            result = session.exec(query).one()
            return result
        except NoResultFound:
            return None

    def get_atleta(self, atleta_id: int):

        with self.session_factory() as session:
            atletas_with_contrato = (
                session.exec(
                    select(Atleta)
                    .options(
                        joinedload(Atleta.contrato).joinedload(
                            Contrato.contrato_sub_tipo
                        )
                    )
                    .where(Atleta.id == atleta_id)
                )
                .unique()
                .all()
            )

            if not atletas_with_contrato:
                return None

            additional_info = session.exec(
                select(
                    Atleta.data_nascimento,
                    Posicao.primeira,
                    Posicao.segunda,
                    Posicao.terceira,
                    HistoricoClube.nome.label('clube'),
                    AtletaAvatar.blob_url,
                )
                .outerjoin(Posicao, Atleta.id == Posicao.atleta_id)
                .outerjoin(
                    HistoricoClube, HistoricoClube.atleta_id == Atleta.id
                )
                .outerjoin(AtletaAvatar, AtletaAvatar.atleta_id == Atleta.id)
                .where(
                    Atleta.id == atleta_id, HistoricoClube.data_fim.is_(None)
                )
            ).all()

            # Combine the results together into a list of AtletaDetails
            results = [
                AtletaDetails(
                    atleta=atleta,
                    data_nascimento=info.data_nascimento,
                    primeira_posicao=info.primeira,
                    segunda_posicao=info.segunda,
                    terceira_posicao=info.terceira,
                    clube_atual=info.clube,
                    avatar_url=info.blob_url,
                    contratos=[
                        ContratoDetails(
                            id=contrato.id,
                            data_inicio=contrato.data_inicio,
                            data_termino=contrato.data_termino,
                            observacao=contrato.observacao,
                            versao=contrato.versao,
                            ativo=contrato.ativo,
                            data_criacao=contrato.data_criacao,
                            data_atualizado=contrato.data_atualizado,
                            contrato_sub_tipo_nome=contrato.contrato_sub_tipo.nome
                            if contrato.contrato_sub_tipo
                            else None,
                        )
                        for contrato in atleta.contrato
                    ],
                )
                for atleta, info in zip(atletas_with_contrato, additional_info)
            ]
        try:

            return self._create_atleta_detail_object(
                results[0] if results else None
            )
        except NoResultFound:
            return None
        except MultipleResultsFound:
            raise

    def create_atleta(self, atleta_data: dict) -> dict:
        with self.session_factory() as session:
            try:
                # Criando uma instância de atleta
                new_atleta = Atleta(**atleta_data)

                session.add(new_atleta)
                session.commit()
                session.refresh(new_atleta)

                return {'id': new_atleta.id}
            except Exception:
                session.rollback()
                raise

    def update_atleta(self, atleta_id: int, atleta_data: dict) -> dict:
        with self.session_factory() as session:
            atleta: Atleta = session.exec(
                select(Atleta).where(Atleta.id == atleta_id)
            ).one()

            # Configurando horário da atualização
            data_atualizacao = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S'
            )

            # Preparando os campos de atleta para atualização
            atleta_update_fields = {
                'nome': atleta_data.get('nome', atleta.nome),
                'data_nascimento': atleta_data.get(
                    'data_nascimento', atleta.data_nascimento
                ),
                'ativo': atleta_data.get('ativo', atleta.ativo),
                'data_atualizado': data_atualizacao,
            }

            # Apenas inclue campos que são novos para atualizar
            updated_fields = {
                k: v
                for k, v in atleta_update_fields.items()
                if getattr(atleta, k) != v
            }

            # Faz a atualização se existirem valores novos para atualizar
            if updated_fields:
                for key, value in updated_fields.items():
                    setattr(atleta, key, value)

            # Faz a atualização de posições se existirem valores novos para atualizar
            posicao = session.exec(
                select(Posicao).where(Posicao.atleta_id == atleta_id)
            ).one()
            posicao.primeira = atleta_data['posicao_primaria']
            posicao.segunda = atleta_data['posicao_secundaria']
            posicao.terceira = atleta_data['posicao_terciaria']
            posicao.data_atualizado = data_atualizacao

            session.commit()

    def save_blob_url(self, atleta_id: int, blob_url: str):
        with self.session_factory() as session:
            user_avatar = session.exec(
                select(AtletaAvatar).filter_by(atleta_id=atleta_id)
            ).first()

            if user_avatar:
                user_avatar.blob_url = blob_url
                user_avatar.data_atualizado = datetime.now(
                    pytz.timezone('America/Sao_Paulo')
                )
            else:
                user_avatar = AtletaAvatar(
                    blob_url=blob_url, atleta_id=atleta_id
                )
                session.add(user_avatar)

            session.commit()

    def get_blob_url(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(AtletaAvatar).where(
                AtletaAvatar.atleta_id == atleta_id
            )

        try:
            result = session.exec(query).one()
            return result.blob_url
        except NoResultFound:
            return None
