from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class LesaoBaseSchema(BaseModel):
    data_lesao: str
    data_retorno: str | None
    descricao: str

    @field_validator('data_lesao', 'data_retorno')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError(
                    'Formato de data inválido, utilize YYYY-MM-DD'
                )


class LesaoCreateSchema(LesaoBaseSchema):
    atleta_id: int = Field(..., gt=0)


class LesaoUpdateSchema(BaseModel):
    lesao_id: int = Field(..., gt=0)


class LesaoCreateResponse(BaseModel):
    id: int
