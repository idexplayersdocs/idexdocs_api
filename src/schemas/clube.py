from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ClubeBaseSchema(BaseModel):
    nome: str
    data_inicio: str
    clube_atual: bool
    data_fim: str

    @field_validator('data_inicio', 'data_fim')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(
                    'Formato de data inválido, utilize YYYY-MM-DD'
                )


class ClubeCreateSchema(ClubeBaseSchema):
    atleta_id: int = Field(..., gt=0)


class ClubeUpdateSchema(BaseModel):
    clube_id: int = Field(..., gt=0)
    

class ClubeCreateResponse(BaseModel):
    id: int
