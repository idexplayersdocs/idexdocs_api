from sqlmodel import Session, SQLModel, create_engine

from src.settings import Settings

settings = Settings()

class BaseSQL:
    """Postgres repository"""

    def __init__(self):
        self._connection_string = 'mssql+pyodbc://{}:{}@{}/{}?TrustServerCertificate=yes&driver=ODBC+Driver+18+for+SQL+Server'.format(
            settings.MSSQL_USER,
            settings.MSSQL_SA_PASSWORD,
            settings.MSSQL_HOSTNAME,
            settings.APPLICATION_DB,
        )

        self.engine = create_engine(self._connection_string)
        SQLModel.metadata.create_all(self.engine)


base = BaseSQL()

engine = base.engine


def create_session(*, expire_on_commit=True):
    return Session(bind=engine, expire_on_commit=expire_on_commit)
