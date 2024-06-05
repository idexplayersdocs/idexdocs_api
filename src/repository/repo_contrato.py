from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select, update

from src.repository.model_objects import (
    Contrato,
    ContratoSubTipo,
    ContratoTipo,
    ContratoVersao,
    datetime_now_sec,
)

from .base_repo import create_session


class ContratoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_contrato_objects(self, result: list) -> list[dict]:
        contrato_list = [
            {
                'contrato_id': id_,
                'contrato_tipo': tipo,
                'contrato_nome': nome,
                'versao': versao,
                'observacao': observacao,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_termino': data_termino.strftime('%Y-%m-%d'),
                'ativo': ativo,
            }
            for id_, tipo, nome, versao, observacao, data_inicio, data_termino, ativo in result
        ]

        return contrato_list

    def _create_contrato_versao_objects(self, result: list) -> list[dict]:
        contrato_list = [
            {
                'versao': versao,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_termino': data_termino.strftime('%Y-%m-%d'),
                'observacao': observacao,
            }
            for versao, data_inicio, data_termino, observacao in result
        ]

        return contrato_list

    def list_contrato(self, atleta_id: int, filters: dict):
        with self.session_factory() as session:
            query = (
                select(
                    Contrato.id,
                    ContratoTipo.tipo,
                    ContratoSubTipo.nome,
                    Contrato.versao,
                    Contrato.observacao,
                    Contrato.data_inicio,
                    Contrato.data_termino,
                    Contrato.ativo,
                )
                .select_from(Contrato)
                .join(
                    ContratoSubTipo,
                    Contrato.contrato_sub_tipo_id == ContratoSubTipo.id,
                )
                .join(
                    ContratoTipo,
                    ContratoSubTipo.contrato_tipo_id == ContratoTipo.id,
                )
                .where(Contrato.atleta_id == atleta_id)
            )

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Contrato.data_termino)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

        return total_count, self._create_contrato_objects(paginated_results)

    def list_contrato_versao(self, contrato_id: int, filters: dict):
        with self.session_factory() as session:
            query = select(
                ContratoVersao.versao,
                ContratoVersao.data_inicio,
                ContratoVersao.data_termino,
                ContratoVersao.observacao,
            ).where(ContratoVersao.contrato_id == contrato_id)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(ContratoVersao.versao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_contrato_versao_objects(
                paginated_results
            )

    def list_contrato_tipo(self) -> dict:
        with self.session_factory() as session:
            query = select(ContratoTipo).options(
                joinedload(ContratoTipo.contrato_sub_tipos)
            )
            result = session.exec(query).unique().all()

            contrato_tipos_list = []
            for contrato_tipo in result:
                contrato_dict = {
                    'id': contrato_tipo.id,
                    'tipo': contrato_tipo.tipo,
                    'contrato_sub_tipos': [
                        {
                            'id': contrato_sub_tipo.id,
                            'nome': contrato_sub_tipo.nome,
                        }
                        for contrato_sub_tipo in contrato_tipo.contrato_sub_tipos
                    ],
                }
                contrato_tipos_list.append(contrato_dict)

            # The final dictionary containing the list of ContratoTipos
            contratos_data = {'contrato_tipos': contrato_tipos_list}

            return contratos_data

    def create_contrato(self, contrato_data: dict) -> dict:
        with self.session_factory() as session:
            try:

                new_contrato = Contrato(**contrato_data)

                session.add(new_contrato)
                session.commit()
                session.refresh(new_contrato)

                new_contrato_versao = ContratoVersao(
                    contrato_id=new_contrato.id,
                    versao=1,
                    data_inicio=contrato_data.get('data_inicio'),
                    data_termino=contrato_data.get('data_termino'),
                    observacao=contrato_data.get('observacao'),
                )

                session.add(new_contrato_versao)
                session.commit()

                return {'id': new_contrato.id}

            except Exception:
                session.rollback()
                raise

    def update_contrato(self, contrato_data: dict) -> dict:
        with self.session_factory() as session:
            contrato_id = contrato_data.get('contrato_id')

            contrato_partial = session.exec(
                select(Contrato.id, Contrato.versao).where(
                    Contrato.id == contrato_id
                )
            ).one()

            # Incrementar versão diretamente, evitando variáveis intermediárias desnecessárias
            contrato_nova_versao = contrato_partial.versao + 1

            # Preparar dados que serão atualizados e adicionados à sessão
            session.exec(
                update(Contrato)
                .where(Contrato.id == contrato_id)
                .values(
                    versao=contrato_nova_versao,
                    data_inicio=contrato_data.get('data_inicio'),
                    data_termino=contrato_data.get('data_termino'),
                    data_atualizado=datetime_now_sec(),
                    observacao=contrato_data.get('observacao'),
                    ativo=contrato_data.get('ativo'),
                )
            )

            new_contrato_versao = ContratoVersao(
                contrato_id=contrato_partial.id,
                versao=contrato_nova_versao,
                data_inicio=contrato_data.get('data_inicio'),
                data_termino=contrato_data.get('data_termino'),
                observacao=contrato_data.get('observacao'),
            )

            session.add(new_contrato_versao)
            session.commit()

    def get_contrato_by_tipo_e_atleta(self, atleta_id: int, contrato_id: int):
        with self.session_factory() as session:
            query = (
                select(Contrato, ContratoSubTipo.nome)
                .join(ContratoSubTipo)
                .where(
                    Contrato.atleta_id == atleta_id,
                    Contrato.contrato_sub_tipo_id == contrato_id,
                )
            )

        try:
            result = session.exec(query).one()
            return result
        except NoResultFound:
            return None
