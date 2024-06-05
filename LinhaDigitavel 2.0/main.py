"""
Script principal que faz a consulta dos dados do banco de dados,
processa e faz requisições para a API de boleto,
e salva as respostas da API em um arquivo Excel.
"""

from Conexoes.ConexaoDB import DatabaseConfig
from Operacao_DB.Consulta_DB import ConsultaDB
from Operacao_DB.Update_linha_digitave import save_to_excel
from Requisioes.ApiRequest import process_and_request_api

def main():
    # Configuração do banco de dados
    db_config = DatabaseConfig()

    # Obtenha os dados do banco de dados
    consulta_db = ConsultaDB(db_config)
    email_data_list = consulta_db.get_data()

    # Crie a engine do SQLAlchemy
    engine = db_config.get_engine()

    # Processa e faz requisições para a API
    process_and_request_api(engine, email_data_list)

    

if __name__ == "__main__":
    main()

