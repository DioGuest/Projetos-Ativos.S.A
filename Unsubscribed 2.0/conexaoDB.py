
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()


# Função para conexão com o banco de dados SQL Server
def get_db_connection():
    # Configuração da conexão com o SQL Server
    server = os.getenv('SERVER_DB')
    database = os.getenv('DATABASE_DB')
    username = os.getenv('USERNAME_DB')
    password = os.getenv('PASSWORD_DB')
    driver = os.getenv('DRIVER_DB')

    # String de conexão
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Conexão com o banco de dados
    conn = pyodbc.connect(conn_str)

    return conn
