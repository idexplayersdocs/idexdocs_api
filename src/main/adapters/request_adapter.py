from typing import Callable

from fastapi import Request

from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


async def request_adapter(
    request: Request, controller: Callable
) -> HttpResponse:
    """Adapter for the request object. The ideia isa to create a layers to
    receive a request object no metter the web framework used: Flask, Django, FastAPI

    Args:
        request (Object): The actual web framework request object

    Returns:
        HttpRequest: Instance of HttpRequest
    """
    http_request = HttpRequest(
        headers=request.headers,
        data=request.body,
        json=await request.json()
        if request.method in ['POST', 'PUT'] and not await request.form()
        else None,
        query_params=request.query_params,
        path_params=request.path_params,
        url=request.url,
        files=await request.form(),
    )

    http_response = controller(http_request)

    return http_response
