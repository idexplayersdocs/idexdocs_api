from pydantic import BaseModel, EmailStr, Field


class UsuarioCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    password: str
    usuario_tipo_id: int = Field(..., ge=1, le=3)


class UsuarioCreateResponse(BaseModel):
    id: int


class UsuarioUpdateSchema(BaseModel):
    id: int = Field(..., ge=1)
    nome: str
    email: EmailStr
    usuario_tipo_id: int = Field(..., ge=1, le=3)


class UsuarioUpdateResponse(BaseModel):
    nome: str
    email: str
    usuario_tipo_id: int


class UsuarioUpdatePasswordSchema(BaseModel):
    id: int = Field(..., ge=1)
    password: str
    new_password: str

class UsuarioUpdatePasswordResponse(BaseModel):
    status: bool
    message: str