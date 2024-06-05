from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ContratoCreateSchema(BaseModel):
    atleta_id: int = Field(..., ge=1)
    contrato_sub_tipo_id: int = Field(..., ge=1)
    data_inicio: str
    data_termino: str
    observacao: str | None = None

    @field_validator('data_inicio', 'data_termino')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class ContratoCreateResponse(BaseModel):
    id: int


class ContratoUpdateSchema(BaseModel):
    contrato_id: int = Field(..., ge=1)
    data_inicio: str
    data_termino: str
    ativo: bool | None = True
    observacao: str | None = None

    @field_validator('data_inicio', 'data_termino')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class ContratoSubTipo(BaseModel):
    id: int
    nome: str


class ContratoTipo(BaseModel):
    id: int
    tipo: str
    contrato_sub_tipos: list[ContratoSubTipo]


class ContratoTipoResponse(BaseModel):
    contrato_tipos: ContratoTipo
