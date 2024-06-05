from abc import ABC, abstractmethod

from ..http_types.http_request import HttpRequest
from ..http_types.http_response import HttpResponse


class ControllerInterface(ABC):
    @abstractmethod
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        ...
