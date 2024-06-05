import pandas as pd
from sqlalchemy import text


def update_linha_digitavel(engine, id_emailing, linha_digitavel):
    """
    Atualiza ou insere a linha digitável do emailing no banco de dados.

    Parâmetros:
    - engine (sqlalchemy.engine.Engine): conexão com o banco de dados.
    - id_emailing (int): identificador do emailing.
    - linha_digitavel (str): linha digitável a ser atualizada ou inserida.
    """
    try:
        # Verifica se a linha digitável já existe no banco de dados
        sql_check_existence = """
        SELECT COUNT(*) FROM [dbo].[tbl_emailing_campos]
        WHERE id_emailing = :id_emailing AND chave = 'linhaDigitavel'
        """
        with engine.connect() as connection:
            result = connection.execute(text(sql_check_existence), {'id_emailing': id_emailing})
            exists = result.scalar() > 0

        if exists:
            # Atualiza a linha digitável existente
            sql_update = """
            UPDATE [dbo].[tbl_emailing_campos]
            SET valor = :linha_digitavel
            WHERE id_emailing = :id_emailing AND chave = 'linhaDigitavel'
            """
            with engine.connect() as connection:
                transaction = connection.begin()
                try:
                    connection.execute(text(sql_update), {'linha_digitavel': linha_digitavel, 'id_emailing': id_emailing})
                    transaction.commit()
                    print(f"Linha digitável '{linha_digitavel}' atualizada para id_emailing {id_emailing}")
                except Exception as e:
                    transaction.rollback()
                    print(f"Erro ao atualizar linha digitável para id_emailing {id_emailing}: {e}")
        else:
            # Insere uma nova linha digitável
            sql_insert = """
            INSERT INTO [dbo].[tbl_emailing_campos] (id_emailing, chave, valor)
            VALUES (:id_emailing, 'linhaDigitavel', :linha_digitavel)
            """
            with engine.connect() as connection:
                transaction = connection.begin()
                try:
                    connection.execute(text(sql_insert), {'id_emailing': id_emailing, 'linha_digitavel': linha_digitavel})
                    transaction.commit()
                    print(f"Linha digitável '{linha_digitavel}' inserida para id_emailing {id_emailing}")
                except Exception as e:
                    transaction.rollback()
                    print(f"Erro ao inserir linha digitável para id_emailing {id_emailing}: {e}")
    except Exception as e:
        print(f"Erro ao conectar para atualizar linha digitável: {e}")


def save_to_excel(api_responses, file_name='respostas_api.xlsx'):
    """
    Salva as respostas da API em um arquivo Excel.

    Parâmetros:
    - api_responses (list): lista de respostas da API.
    - file_name (str): nome do arquivo Excel para salvar as respostas (opcional, default='respostas_api.xlsx').
    """
    df = pd.DataFrame(api_responses)
    df.to_excel(file_name, index=False)
    print("Informações da API foram salvas em:", file_name)

