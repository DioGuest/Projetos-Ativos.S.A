import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker

class DatabaseConfig:
    """
    Classe responsável por configurar a conexão com o banco de dados.
    """
    def __init__(self):
        """
        Inicializa a instância da classe DatabaseConfig.
        Carrega as variáveis de ambiente do arquivo .env e cria a string de conexão.
        """
        load_dotenv()  # Carregar variáveis de ambiente do arquivo .env
        self.username_db = os.getenv('USERNAME_DB')
        self.password_db = os.getenv('PASSWORD_DB')
        self.servidor_db = os.getenv('SERVIDOR_DB')
        self.base_db = os.getenv('BASE_DB')
        self.driver_db = os.getenv('DRIVER_DB')
        self.connection_string = (
            f"mssql+pyodbc://{self.username_db}:{self.password_db}@"
            f"{self.servidor_db}/{self.base_db}?driver={self.driver_db}"
        )

    def get_engine(self):
        """
        Retorna um objeto Engine do SQLAlchemy para a conexão com o banco de dados.
        """
        self.engine = sqlalchemy.create_engine(self.connection_string)
        return self.engine

    def get_session(self):
        """
        Retorna uma sessão de conexão com o banco de dados.
        """
        self.engine = self.get_engine()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session



