from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo


class CaracteristicaCreateUseCase:
    def __init__(
        self,
        atleta_repository: AtletaRepo,
        caracteristica_repository: CaracteristicasRepo,
    ):
        self.atleta_repository = atleta_repository
        self.caracteristica_repository = caracteristica_repository

    def execute(self, http_request: HttpRequest):
        caracteristica_data: dict = http_request.json

        atleta_id: int = caracteristica_data.get('atleta_id')
        model_name: int = caracteristica_data.pop('caracteristica')

        self._check_atleta_exists(atleta_id)

        result = self._create_caracteristica(caracteristica_data, model_name)

        return result

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _create_caracteristica(
        self, atleta_data: dict, model_name: str
    ) -> dict:
        return self.caracteristica_repository.create_caracteristica(
            atleta_data, model_name
        )
