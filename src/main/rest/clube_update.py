from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.clube_update_composer import clube_update_composer
from src.schemas.clube import ClubeUpdateSchema
from src.validators.validate_schema import validate_schema


async def clube_update(request: Request):
    try:
        await validate_schema(request, ClubeUpdateSchema)
        http_response = await request_adapter(request, clube_update_composer())
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
