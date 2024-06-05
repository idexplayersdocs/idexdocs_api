from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.files_update_composer import update_files_composer
from src.schemas.file_upload import FileUpdateSchema
from src.validators import validate_schema


async def imagem_update(request: Request):
    try:
        await validate_schema(request, FileUpdateSchema)
        http_response = await request_adapter(
            request, update_files_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
