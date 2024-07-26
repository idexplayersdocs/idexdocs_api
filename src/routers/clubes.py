from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import session_context
from src.main.composers.clube_create_composer import clube_create_composer
from src.main.composers.clube_list_composer import clube_list_composer
from src.schemas.clube import ClubeCreateSchema

router = APIRouter(prefix='/clubes', tags=['clube'])
T_Session = Annotated[Session, Depends(session_context)]



@router.post('/', status_code=HTTPStatus.CREATED)
def create_clube(clube: ClubeCreateSchema, session: T_Session):
    

    clube_dict = clube.model_dump()

    return clube_create_composer(clube_dict, session).body

@router.get('/{atleta_id}')
def list_clube(atleta_id: int, session: T_Session):



    return clube_list_composer({'atleta_id': atleta_id},session).body