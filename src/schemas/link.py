from pydantic import BaseModel, HttpUrl, ValidationError, field_validator


class LinkCreateSchema(BaseModel):
    atleta_id: int
    url: str
    descricao: str

    @field_validator('url')
    def validar_url(cls, v):
        try:
            # Tenta validar como HttpUrl
            HttpUrl(v)
        except ValidationError:
            raise ValueError('Formato de URL inválido. Use um link HTTP ou HTTPS válido.')
        return v

    @field_validator('descricao')
    def descricao_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Insira um valor para o campo descrição')
        return v
    
class LinkResponseSchema(BaseModel):
    id: int