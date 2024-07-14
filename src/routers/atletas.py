from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import session_context
from src.main.composers.atleta_create_composer import atleta_create_composer
from src.main.composers.atleta_list_composer import atleta_list_composer
from src.main.composers.atleta_update_composer import atleta_update_composer
from src.repository.model_objects import Usuario
from src.schemas.atleta import (
    AtletaCreateResponse,
    AtletaCreateSchema,
    AtletaListResponse,
)
from src.security.security import get_current_user

router = APIRouter(prefix='/atletas', tags=['atleta'])
T_Session = Annotated[Session, Depends(session_context)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED)
def create_atleta(
    atleta: AtletaCreateSchema,
    session: T_Session,
    # current_user: T_CurrentUser
):

    atleta_dict = atleta.model_dump()

    return atleta_create_composer(atleta_dict, session).body


@router.get('/', status_code=HTTPStatus.OK, response_model=AtletaListResponse)
def list_atleta(
    session: T_Session,
    # current_user: T_CurrentUser,
    page: int = 1,
    per_page: int = 10,
):

    return atleta_list_composer(
        {'page': page, 'per_page': per_page}, session
    ).body


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=AtletaCreateResponse)
def upadte_atleta(
    id: int,
    atleta: AtletaCreateSchema,
    session: T_Session,
    # current_user: T_CurrentUser
    ):
    
    atleta_dict = atleta.model_dump()

    return atleta_update_composer({'id': id, 'atleta': atleta_dict}, session).body
