from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ClubeCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    nome: str
    data_inicio: str
    clube_atual: bool
    data_fim: str | None

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


class ClubeCreateResponse(BaseModel):
    id: int
