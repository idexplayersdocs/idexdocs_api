from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class RelacionamentoCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    receptividade_contrato: int = Field(..., ge=1, le=5)
    satisfacao_empresa: int = Field(..., ge=1, le=5)
    satisfacao_clube: int = Field(..., ge=1, le=5)
    relacao_familiares: int = Field(..., ge=1, le=5)
    influencias_externas: int = Field(..., ge=1, le=5)
    pendencia_empresa: bool
    pendencia_clube: bool
    data_avaliacao: str

    @field_validator('data_avaliacao')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class RelacionamentoResponse(BaseModel):
    id: int
