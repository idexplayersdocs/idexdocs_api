from .base_repo import create_session
from .model_objects import Posicao


class PosicaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def create_posicao(self, posicao_data: dict) -> dict:
        with self.session_factory() as session:
            new_posicao = Posicao(**posicao_data)
            session.add(new_posicao)
            session.commit()
            session.refresh(new_posicao)
            return {'id': new_posicao.id}
