"""Modulo para adaptação do objeto response para a aplicação
"""
from dataclasses import dataclass
from enum import Enum


class HttpStatusCode(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500


@dataclass
class HttpResponse:
    body: str
    status_code: int = HttpStatusCode
