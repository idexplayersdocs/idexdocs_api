from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.lesao_create_composer import lesao_create_composer
from src.schemas.lesao import LesaoCreateSchema
from src.validators.validate_schema import validate_schema


async def lesao_create(request: Request):
    try:
        await validate_schema(request, LesaoCreateSchema)
        http_response = await request_adapter(request, lesao_create_composer())
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
