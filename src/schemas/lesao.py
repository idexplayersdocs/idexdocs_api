from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class LesaoCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    data_lesao: str
    data_retorno: str
    descricao: str

    @field_validator('data_lesao')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(
                    'Formato de data inválido, utilize YYYY-MM-DD'
                )


class LesaoCreateResponse(BaseModel):
    id: int
