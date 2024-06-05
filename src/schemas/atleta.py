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
    nome: str
    data_inicio: str

    _validate_data_inicio = field_validator('data_inicio')(
        validate_date_format
    )


class Contrato(BaseModel):
    contrato_sub_tipo_id: int
    data_inicio: str
    data_termino: str
    observacao: str | None = None

    _validate_data_inicio = field_validator('data_inicio')(
        validate_date_format
    )
    _validate_data_fim = field_validator('data_termino')(validate_date_format)


class AtletaCreateSchema(BaseModel):
    nome: str
    data_nascimento: str
    clube: Clube
    contrato_clube: Contrato
    contrato_empresa: Contrato
    posicao_primaria: str
    posicao_secundaria: str | None
    posicao_terciaria: str | None

    _validate_data_nascimento = field_validator('data_nascimento')(
        validate_date_format
    )

    @field_validator(
        'posicao_primaria', 'posicao_secundaria', 'posicao_terciaria'
    )
    def validate_posicao_id(cls, v):
        allowed_positions = (
            'atacante',
            'goleiro',
            'lateral',
            'meia',
            'volante',
            'zagueiro',
        )
        if v and v not in allowed_positions:
            raise ValueError(
                f'Posição inválida: {v}. Posições permitidas: {allowed_positions}'
            )
        return v


class AtletaCreateResponse(BaseModel):
    id: int


class AtletaUpdateSchema(BaseModel):
    nome: str
    data_nascimento: str
    posicao_primaria: str
    posicao_secundaria: str | None
    posicao_terciaria: str | None
    ativo: bool

    _validate_data_nascimento = field_validator('data_nascimento')(
        validate_date_format
    )
