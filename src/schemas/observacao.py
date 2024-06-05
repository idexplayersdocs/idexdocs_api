from enum import Enum

from pydantic import BaseModel, Field


class ObservacaoTypes(str, Enum):
    desempenho = 'desempenho'
    relacionamento = 'relacionamento'


class ObservacaoCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    tipo: ObservacaoTypes
    descricao: str


class ObservacaoCreateResponse(BaseModel):
    id: int


class ObservacaoListSchema(BaseModel):
    atleta_id: int
    tipo: str
    descricao: str
    data_observacao: str


class ObservacaoListResponse(BaseModel):
    count: int
    type: str
    data: list[ObservacaoListSchema]
