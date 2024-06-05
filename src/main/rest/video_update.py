from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.video_update_composer import video_update_composer
from src.schemas.video import VideoUpdateSchema
from src.validators import validate_schema


async def video_update(request: Request):
    try:
        await validate_schema(request, VideoUpdateSchema)
        http_response = await request_adapter(request, video_update_composer())
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
