from datetime import datetime

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import Permissao, Usuario, UsuarioPermissao, UsuarioTipo


class UsuarioRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_usuario_objects(self, result: list) -> list[dict]:

        usuario_list = [
            {
                'id': usuario.get('id'),
                'nome': usuario.get('nome'),
                'email': usuario.get('email'),
                'data_criacao': usuario.get('data_criacao').strftime(
                    '%Y-%m-%d'
                ),
                'tipo': usuario.get('tipo'),
                'permissoes': usuario.get('permissoes'),
            }
            for usuario in result
        ]

        return usuario_list

    def _create_usuario_token_objects(self, usuario: Usuario) -> list[dict]:
        usuario = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'data_criacao': usuario.data_criacao.strftime('%Y-%m-%d'),
            'hash_password': usuario.hash_password,
            'tipo': usuario.tipo.value,
        }

        return usuario

    def create_usuario(self, usuario_data: dict) -> dict:
        with self.session_factory() as session:
            usuario_permissoes = usuario_data.pop('permissoes')

            new_usuario = Usuario(**usuario_data)
            session.add(new_usuario)
            session.commit()
            session.refresh(new_usuario)

            def get_permission_by_name(nome: str) -> Permissao | None:
                return session.exec(
                    select(Permissao).filter_by(nome=nome)
                ).first()

            for perm_name, has_permission in usuario_permissoes.items():
                if has_permission:
                    permissao = get_permission_by_name(perm_name)
                    if permissao:
                        new_perm_assoc = UsuarioPermissao(
                            usuario_id=new_usuario.id,
                            permissao_id=permissao.id,
                        )
                        session.add(new_perm_assoc)
            session.commit()

            return {'id': new_usuario.id}

    def get_usuario_by_email(self, usuario_email: str) -> dict:
        with self.session_factory() as session:
            query = (
                select(
                    Usuario.id,
                    Usuario.nome,
                    Usuario.email,
                    Usuario.data_criacao,
                    Usuario.hash_password,
                    UsuarioTipo.tipo,
                )
                .join(UsuarioTipo)
                .where(Usuario.email == usuario_email)
            )

        try:
            result = session.exec(query).one()
            return self._create_usuario_token_objects(result)
        except NoResultFound:
            return None

    def get_usuario_by_id(self, usuario_id: int) -> dict:
        with self.session_factory() as session:
            query = (
                select(
                    Usuario.id,
                    Usuario.nome,
                    Usuario.email,
                    Usuario.data_criacao,
                    Usuario.hash_password,
                    UsuarioTipo.tipo,
                )
                .join(UsuarioTipo)
                .where(Usuario.id == usuario_id)
            )

        try:
            result = session.exec(query).one()
            return self._create_usuario_token_objects(result)
        except NoResultFound:
            return None

    def list_usuario(self, filters: dict = {}):
        with self.session_factory() as session:
            query = select(Usuario).options(
                joinedload(Usuario.permissoes).joinedload(
                    UsuarioPermissao.permissao
                ),
                selectinload(Usuario.tipo_usuario),  # Eager load UsuarioTipo
            )

            # Conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # Aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Usuario.nome)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # Executa query com paginação
            usuarios = session.exec(query).unique().all()

            # Fetch all permissions only once to avoid repeated queries
            all_permissions = {
                permissao.nome: False
                for permissao in session.exec(select(Permissao)).all()
            }

            usuarios_data = []
            for usuario in usuarios:
                perm_dict = all_permissions.copy()

                for usuario_permissao in usuario.permissoes:
                    perm_dict[usuario_permissao.permissao.nome] = True

                usuario_info = {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'data_criacao': usuario.data_criacao,
                    'tipo': usuario.tipo_usuario.tipo.value
                    if usuario.tipo_usuario
                    else None,
                    'permissoes': perm_dict,
                }

                usuarios_data.append(usuario_info)

            return total_count, self._create_usuario_objects(usuarios_data)

    def update_usuario(self, usuario_id: int, usuario_data: dict) -> dict:
        with self.session_factory() as session:
            usuario: Usuario = session.exec(
                select(Usuario).where(Usuario.id == usuario_id)
            ).one()

            usuario.nome = usuario_data.get('nome')
            usuario.email = usuario_data.get('email')
            usuario.usuario_tipo_id = usuario_data.get('usuario_tipo_id')
            usuario.data_atualizado = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S'
            )

            def get_permission_by_name(nome: str) -> Permissao | None:
                return session.exec(
                    select(Permissao).filter_by(nome=nome)
                ).first()

            for permission_name, should_have_permission in usuario_data.get(
                'permissoes'
            ).items():
                permissao = get_permission_by_name(permission_name)

                usuario_permissao = session.exec(
                    select(UsuarioPermissao).filter_by(
                        usuario_id=usuario.id, permissao_id=permissao.id
                    )
                ).first()

                if should_have_permission and not usuario_permissao:
                    new_perm_assoc = UsuarioPermissao(
                        usuario_id=usuario.id,
                        permissao_id=permissao.id,
                    )
                    session.add(new_perm_assoc)
                elif not should_have_permission and usuario_permissao:
                    session.delete(usuario_permissao)

            session.commit()

    def update_usurio_password(self, usuario_id: int, new_password: str):
        with self.session_factory() as session:
            try:
                usuario: Usuario = session.exec(
                    select(Usuario).where(Usuario.id == usuario_id)
                ).one()

                usuario.hash_password = new_password
                session.commit()
                return {
                    'status': True,
                    'message': 'Senha alterada com sucesso',
                }
            except Exception:
                session.rollback()
                return {'status': False, 'message': 'Operação não realizada'}
