from src.presentation.controllers.pdf_create import PdfCreateController
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo
from src.repository.repo_clube import ClubeRepo
from src.repository.repo_competicao import CompeticaoRepo
from src.repository.repo_controle import ControleRepo
from src.repository.repo_lesao import LesaoRepo
from src.repository.repo_observacao import ObservacaoRepo
from src.repository.repo_relacionamento import RelacionamentoRepo
from src.use_cases.caracteristica_list import CaracteristicaListUseCase
from src.use_cases.pdf_create import PdfCreateUseCase


def pdf_create_composer():
    clube_repository = ClubeRepo()
    lesao_repository = LesaoRepo()
    atleta_repository = AtletaRepo()
    controle_repository = ControleRepo()
    competicao_repository = CompeticaoRepo()
    observacao_repository = ObservacaoRepo()
    relacionamento_repository = RelacionamentoRepo()
    caracteristica_repository = CaracteristicasRepo()
    caracteristica_repository = CaracteristicasRepo()

    caracteristica_use_case = CaracteristicaListUseCase(
        atleta_repository=atleta_repository,
        caracteristica_repository=caracteristica_repository,
    )

    use_case = PdfCreateUseCase(
        clube_repository=clube_repository,
        lesao_repository=lesao_repository,
        atleta_repository=atleta_repository,
        controle_repository=controle_repository,
        competicao_repository=competicao_repository,
        observacao_repository=observacao_repository,
        caracteristica_use_case=caracteristica_use_case,
        caracteristica_repository=caracteristica_repository,
        relacionamento_repository=relacionamento_repository,
    )
    controller = PdfCreateController(use_case=use_case)

    return controller.handle
