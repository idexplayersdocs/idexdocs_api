from pydantic import BaseModel


class VideoCreateSchema(BaseModel):
    video_url: str


class VideoUpdateSchema(BaseModel):
    video_id: int
    descricao: str
