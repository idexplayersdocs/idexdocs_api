from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta

import pytz
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlmodel import and_, func, select

from .base_repo import create_session
from .model_objects import (
    Atleta,
    AtletaAvatar,
    AtletaPosicao,
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
                'posicao_primaria': posicao,
                'clube_atual': clube,
                'data_proxima_avaliacao_relacionamento': (
                    data_avaliacao + timedelta(days=30)
                ).strftime('%Y-%m-%d')
                if data_avaliacao
                else None,
                'ativo': ativo,
            }
            for id_, nome, data_nascimento, posicao, clube, data_avaliacao, ativo in result
        ]

    def _create_atleta_detail_object(self, result: AtletaDetails) -> dict:
        return {
            'nome': result.atleta.nome,
            'data_nascimento': result.atleta.data_nascimento.strftime(
                '%Y-%m-%d'
            ),
            'posicao_primaria': result.primeira_posicao
            if result.primeira_posicao
            else None,
            'posicao_secundaria': result.segunda_posicao
            if result.segunda_posicao
            else None,
            'posicao_terciaria': result.terceira_posicao
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

            posicao_subquery = (
                select(AtletaPosicao.atleta_id, Posicao.nome)
                .outerjoin(Posicao, Posicao.id == AtletaPosicao.posicao_id)
                .where(AtletaPosicao.preferencia == 'primeira')
                .subquery()
            )

            query = (
                select(
                    Atleta.id.label('id_'),
                    Atleta.nome.label('nome'),
                    Atleta.data_nascimento.label('data_nascimento'),
                    posicao_subquery.c.nome,
                    HistoricoClube.nome.label('clube'),
                    Relacionamento.data_avaliacao,
                    Atleta.ativo,
                )
                .select_from(Atleta)
                .outerjoin(
                    HistoricoClube,
                    and_(
                        HistoricoClube.atleta_id == Atleta.id,
                        HistoricoClube.clube_atual == 1,
                    ),
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
                .outerjoin(
                    posicao_subquery, posicao_subquery.c.atleta_id == Atleta.id
                )
                .order_by(Atleta.id)
            )

            if atleta := filters.get('atleta'):
                query = query.where(Atleta.nome.contains(atleta))

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

            # Retorna caso não exista atleta
            if not atletas_with_contrato:
                return None

            atleta_with_posicao = (
                select(AtletaPosicao.preferencia, Posicao.id)
                .join(Posicao, Posicao.id == AtletaPosicao.posicao_id)
                .where(AtletaPosicao.atleta_id == atleta_id)
            )
            posicoes = session.exec(atleta_with_posicao).all()
            posicao_mapping = {
                preferencia: nome_posicao
                for preferencia, nome_posicao in posicoes
            }

            atleta_additional_info = session.exec(
                select(
                    Atleta.data_nascimento,
                    HistoricoClube.nome.label('clube'),
                    AtletaAvatar.blob_url,
                )
                .outerjoin(
                    HistoricoClube,
                    and_(
                        HistoricoClube.atleta_id == Atleta.id,
                        HistoricoClube.clube_atual == 1,
                    ),
                )
                .outerjoin(AtletaAvatar, AtletaAvatar.atleta_id == Atleta.id)
                .where(Atleta.id == atleta_id)
            ).all()

            # Combine the results together into a list of AtletaDetails
            results = [
                AtletaDetails(
                    atleta=atleta,
                    data_nascimento=info.data_nascimento,
                    primeira_posicao=posicao_mapping.get('primeira'),
                    segunda_posicao=posicao_mapping.get('segunda'),
                    terceira_posicao=posicao_mapping.get('terceira'),
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
                for atleta, info in zip(
                    atletas_with_contrato, atleta_additional_info
                )
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
        with self.session_factory().no_autoflush as session:
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
            new_posicao = OrderedDict(
                [
                    ('primeira', int(atleta_data.get('posicao_primaria'))),
                    ('segunda', int(atleta_data.get('posicao_secundaria'))),
                    ('terceira', int(atleta_data.get('posicao_terciaria'))),
                ]
            )

            for preferencia, posicao_id in new_posicao.items():
                if posicao_id is not None:
                    existing_posicao = session.exec(
                        select(AtletaPosicao).filter_by(
                            atleta_id=atleta_id, preferencia=preferencia
                        )
                    ).first()
                    if existing_posicao:
                        existing_posicao.posicao_id = posicao_id
                        existing_posicao.data_atualizado = data_atualizacao
                    else:
                        new_posicao = AtletaPosicao(
                            atleta_id=atleta_id,
                            posicao_id=posicao_id,
                            preferencia=preferencia,
                            data_atualizado=data_atualizacao,
                        )
                        session.add(new_posicao)

            session.commit()

        return True

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
