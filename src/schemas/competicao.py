from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CompeticaoCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    nome: str
    data_competicao: str
    jogos_completos: int = Field(..., ge=0)
    jogos_parciais: int = Field(..., ge=0)
    minutagem: int = Field(..., ge=0)
    gols: int = Field(..., ge=0)
    assistencias: int = Field(..., ge=0)

    @field_validator('data_competicao')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class CompeticaoCreateResponse(BaseModel):
    id: int


class CompeticaoListResponse(BaseModel):
    count: int
    tupe: str
    data: list[CompeticaoCreateSchema]
