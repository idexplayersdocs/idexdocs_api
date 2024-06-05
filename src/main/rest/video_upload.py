from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.video_upload_composer import video_upload_composer
from src.schemas.video import VideoCreateSchema
from src.validators import validate_schema


async def video_upload(request: Request):
    try:
        await validate_schema(request, VideoCreateSchema)
        http_response = await request_adapter(request, video_upload_composer())
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
