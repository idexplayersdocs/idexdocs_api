from collections import defaultdict

from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo


class CaracteristicaListUseCase:
    def __init__(
        self,
        atleta_repository: AtletaRepo,
        caracteristica_repository: CaracteristicasRepo,
    ):
        self.atleta_repository = atleta_repository
        self.caracteristica_repository = caracteristica_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)

        result, model_name = self._list_caracteristica(
            atleta_id, filters, filters.get('model')
        )

        return self._format_response(result, model_name)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_caracteristica(
        self, atleta_id: int, filters: dict, model_name: str
    ):
        (
            caracteristicas,
            model_name,
        ) = self.caracteristica_repository.list_caracteristica(
            atleta_id, filters
        )

        # As características físicas não possuem valores para agregação
        agregado = (
            self._agrega_total_e_media(caracteristicas)
            if model_name != 'CaracteristicaFisica'
            else caracteristicas
        )

        return agregado, model_name

    def _agrega_total_e_media(self, caracteristicas: list):
        result = defaultdict(list)
        suffixes = ['_fis', '_tec', '_psi']
        mapper = {'_fis': 'fisico', '_tec': 'tecnico', '_psi': 'psicologico'}

        # Collect keys that don't need processing for sums and means just once
        excluded_keys = {'data_avaliacao'}

        for item in caracteristicas:
            for suffix in suffixes:
                # Extract numeric values and calculate sum and mean separately
                numeric_values = [
                    value
                    for key, value in item.items()
                    if key.endswith(suffix)
                ]
                total = sum(numeric_values)
                mean = total / len(numeric_values) if numeric_values else 0

                # Create a dictionary with the required extracted data
                extracted = {
                    key: value
                    for key, value in item.items()
                    if key.endswith(suffix) or key in excluded_keys
                }
                extracted['sum'] = total
                extracted['mean'] = round(mean, 2)

                result[mapper[suffix]].append(extracted)

        # Initialize a dictionary to hold means for each date
        date_means = defaultdict(list)

        # Collect means per date for all categories
        for category in result.values():
            for item in category:
                date_means[item['data_avaliacao']].append(item['mean'])

        # Calculate the average of averages (assuming there are no dates with zero values)
        total_mean = {
            date: round(sum(means) / len(means), 2)
            for date, means in date_means.items()
        }

        # Add the calculated total_mean to the result
        complete_result = dict(result)
        complete_result['total_mean'] = total_mean

        return complete_result

    def _format_response(self, result: list[dict], model_name: str) -> dict:
        return {
            'type': model_name,
            'data': result,
        }
