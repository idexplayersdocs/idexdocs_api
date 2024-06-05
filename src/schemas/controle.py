from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ControleCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    nome: str
    quantidade: int = Field(..., ge=1)
    preco: Decimal = Field(gt=0, decimal_places=2)
    data_controle: str

    @field_validator('data_controle')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')

    @field_validator('preco')
    def validate_preco(cls, v):
        str_value = f'{v}'
        if '.' not in str_value:
            raise ValueError('O preço deve conter separador .00')
        return v


class ControleCreateResponse(BaseModel):
    id: int


class ControleListResponse(BaseModel):
    count: int
    tupe: str
    data: list[ControleCreateSchema]
