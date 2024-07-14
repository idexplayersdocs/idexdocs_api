from datetime import date, datetime

from pydantic import BaseModel, field_validator


def validate_date_format(date_str: str) -> str:
    if date_str is not None:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class AtletaCreateSchema(BaseModel):
    nome: str
    data_nascimento: str
    posicao_primaria: str
    posicao_secundaria: str
    posicao_terciaria: str

    _validate_data_nascimento = field_validator('data_nascimento')(
        validate_date_format
    )

    @field_validator(
        'posicao_primaria', 'posicao_secundaria', 'posicao_terciaria'
    )
    def validate_posicao_id(cls, v):
        if v and int(v) not in range(1, 11):
            raise ValueError(f'ID de posição inválido: {v}.')
        return v


class AtletaCreateResponse(BaseModel):
    id: int

class AtletaBaseResponse(BaseModel):
    id: int
    nome: str
    data_nascimento: str
    posicao_primaria: str | None
    clube_atual: str | None
    data_proxima_avaliacao_relacionamento: date | None
    ativo: bool

class AtletaListResponse(BaseModel):
    count: int
    total: int
    type: str
    data: list[AtletaBaseResponse]

class AtletaUpdateSchema(AtletaCreateSchema):
    ativo: bool

