from fastapi import Request
from fastapi.responses import JSONResponse

from src.error.error_handler import handle_errors
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.obervacao_list_composer import observacao_list_composer
from src.validators.validate_schema import validate_schema


async def observacao(request: Request):
    try:
        await validate_schema(request)
        http_response = await request_adapter(
            request, observacao_list_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
