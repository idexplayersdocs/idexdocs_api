from datetime import datetime

from pydantic import BaseModel, field_validator


def validate_date_format(date_str: str) -> str:
    if date_str is not None:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class Clube(BaseModel):
    nome: str | None
    data_inicio: str | None

    _validate_data_inicio = field_validator('data_inicio')(
        validate_date_format
    )


class Contrato(BaseModel):
    contrato_sub_tipo_id: int | None
    data_inicio: str | None
    data_termino: str | None
    observacao: str | None = None

    _validate_data_inicio = field_validator('data_inicio')(
        validate_date_format
    )
    _validate_data_fim = field_validator('data_termino')(validate_date_format)


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
        # Existem 12 posições, mas adiciona-se 1 pois o range max é não inclusivo.
        if v and int(v) not in range(1, 12 + 1):
            raise ValueError(f'ID de posição inválido: {v}.')
        return v


class AtletaCreateResponse(BaseModel):
    id: int


class AtletaUpdateSchema(AtletaCreateSchema):
    ativo: bool

