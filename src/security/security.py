from datetime import datetime, timedelta

import pytz
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from src.error.types.credentials_exception import CredentialsException
from src.error.types.http_bad_request import BadRequestError
from src.repository.base_repo import create_session
from src.repository.model_objects import (
    Permissao,
    Role,
    RolePermissao,
    UsuarioPermissao,
    UsuarioRole,
)
from src.repository.repo_usuario import UsuarioRepo

SECRET_KEY = '131e9590439e5e7bc331cfa2044861a21a2e39c021610ae2bfa7c94649d4e771'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
usuario_repository = UsuarioRepo()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = (
            datetime.now(pytz.timezone('America/Sao_Paulo')) + expires_delta
        )
    else:
        expire = datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get('sub')
        roles = payload.get('roles', [])
        permissions = payload.get('permissions', [])
        if not user_email:
            raise CredentialsException(
                'Não foi possível validar as credenciais'
            )
    except JWTError:
        raise CredentialsException('Não foi possível validar as credenciais')
    return {'email': user_email, 'roles': roles, 'permissions': permissions}


def get_user_roles_and_permissions(session: Session, user_id: int):
    # Retrieve roles
    role_statement = (
        select(Role.nome)
        .join(UsuarioRole, UsuarioRole.role_id == Role.id)
        .where(UsuarioRole.usuario_id == user_id)
    )
    roles = session.exec(role_statement).all()

    # Retrieve permissions
    permission_statement = (
        select(Permissao.nome)
        .join(UsuarioPermissao, UsuarioPermissao.permissao_id == Permissao.id)
        .where(UsuarioPermissao.usuario_id == user_id)
    )
    permissions = session.exec(permission_statement).all()

    role_permissions_statement = (
        select(Permissao.nome)
        .join(RolePermissao, RolePermissao.permissao_id == Permissao.id)
        .join(Role, Role.id == RolePermissao.role_id)
        .join(UsuarioRole, UsuarioRole.role_id == Role.id)
        .where(UsuarioRole.usuario_id == user_id)
    )
    role_permissions = session.exec(role_permissions_statement).all()

    all_permissions = set(permissions + role_permissions)

    return roles, all_permissions


def login_user(email: str, password: str):
    user = usuario_repository.get_usuario_by_email(email)
    if not user and not verify_password(password, user['hash_passord']):
        raise BadRequestError('Email ou senha incorretos')

    try:
        with create_session() as session:
            roles, permissions = get_user_roles_and_permissions(
                session, user['id']
            )
    except Exception as e:
        print(f'Erro ao buscar perfis e permissões do usuário: {e}')
        raise

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            'sub': user['email'],
            'user_id': user['id'],
            'user_name': user['nome'],
            'last_login': datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d %H:%M:%S'),
            'roles': roles,
            'permissions': list(permissions),
        },
        expires_delta=access_token_expires,
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
