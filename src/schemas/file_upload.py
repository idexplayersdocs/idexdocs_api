from fastapi import UploadFile
from pydantic import BaseModel


class FileUploadCreateSchema(BaseModel):
    image: UploadFile


class FileUpdateSchema(BaseModel):
    imagem_id: int
    descricao: str