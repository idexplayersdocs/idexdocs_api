from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import get_session
from src.main.composers.atleta_create_composer import atleta_create_composer
from src.repository.repo_atleta import AtletaRepo
from src.schemas.atleta import AtletaCreateSchema

router = APIRouter(prefix='/atletas', tags=['atleta'])
T_Session = Annotated[Session, Depends(get_session)]

atleta_repo = AtletaRepo()

@router.post('/', status_code=HTTPStatus.CREATED)
def create_atleta(data: AtletaCreateSchema, session: T_Session):

    atleta = data.model_dump()
    
    return atleta_create_composer(atleta)

@router.get('/', status_code=HTTPStatus.OK)
def read_atleta():
    ...

@router.put('/', status_code=HTTPStatus.OK)
def upadte_atleta():
    ...

