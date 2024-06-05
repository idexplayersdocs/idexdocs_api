from src.presentation.controllers.caracteristica_list_controler import (
    CaracteristicaListController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo
from src.use_cases.caracteristica_list import CaracteristicaListUseCase


def caracteristica_list_composer():
    atleta_repository = AtletaRepo()
    caracteristica_repository = CaracteristicasRepo()

    use_case = CaracteristicaListUseCase(
        atleta_repository=atleta_repository,
        caracteristica_repository=caracteristica_repository,
    )
    controller = CaracteristicaListController(use_case=use_case)

    return controller.handle
