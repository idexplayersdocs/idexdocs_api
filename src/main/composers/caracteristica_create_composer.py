from src.presentation.controllers.caracteristica_create_controler import (
    CaracteristicaCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo
from src.use_cases.caracteristica_create import CaracteristicaCreateUseCase


def caracteristica_create_composer():
    atleta_repository = AtletaRepo()
    caracteristica_repository = CaracteristicasRepo()

    use_case = CaracteristicaCreateUseCase(
        atleta_repository=atleta_repository,
        caracteristica_repository=caracteristica_repository,
    )
    controller = CaracteristicaCreateController(use_case=use_case)

    return controller.handle
