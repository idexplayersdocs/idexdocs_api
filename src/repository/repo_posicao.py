from .base_repo import create_session
from .model_objects import AtletaPosicao


class PosicaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def create_posicao(self, posicao_data: dict) -> dict:
        with self.session_factory() as session:

            atleta_id = posicao_data.pop('atleta_id')
            for preferencia, posicao_id in posicao_data.items():
                new_posicao = AtletaPosicao(
                    atleta_id=atleta_id,
                    posicao_id=posicao_id,
                    preferencia=preferencia,
                )
                session.add(new_posicao)

            session.commit()
        return True
