from sqlalchemy.sql import text
from Classes.Classe_DB import EmailData
from Conexoes.ConexaoDB import DatabaseConfig


class ConsultaDB:
    """
    Classe responsável por realizar consultas no banco de dados.
    """

    def __init__(self, db_config: DatabaseConfig):
        """
        Inicializa a instância da classe ConsultaDB.

        Parâmetros:
        - db_config (DatabaseConfig): objeto de configuração de conexão com o banco de dados.
        """
        self.db_config = db_config

    def get_session(self):
        """
        Retorna uma sessão de conexão com o banco de dados.

        Retorna:
        - session (Session): sessão de conexão com o banco de dados.
        """
        session = self.db_config.get_session()
        return session

    def get_data(self):
        """
        Realiza uma consulta no banco de dados e retorna uma lista de objetos EmailData.

        Retorna:
        - email_data_list (List[EmailData]): lista de objetos EmailData.
        """
        session = self.get_session()

        # Nova consulta
        query = text("""
            SELECT e.id_emailing, 
                       e.destinatario_ndg,
                       ec.chave AS chave_linhaDigitavel, 
                       ec.valor AS valor_linhaDigitavel, 
                       ec1.chave AS chave_numAcordo, 
                       ec1.valor AS valor_numAcordo, 
                       ec2.chave AS chave_num_parcela, 
                       ec2.valor AS valor_num_parcela
            FROM [MS-CTL-MAIL].[dbo].[tbl_emailing] e
            INNER JOIN [dbo].[tbl_emailing_layout_campos] elc 
                ON e.id_layout = elc.id_layout
                AND elc.chave = 'linhaDigitavel'
            LEFT JOIN [MS-CTL-MAIL].[dbo].tbl_emailing_campos ec 
                ON e.id_emailing = ec.id_emailing 
                AND elc.chave = ec.chave 
            LEFT JOIN [MS-CTL-MAIL].[dbo].tbl_emailing_campos ec1 
                ON e.id_emailing = ec1.id_emailing 
                AND ec1.chave = 'numAcordo'
            LEFT JOIN [MS-CTL-MAIL].[dbo].tbl_emailing_campos ec2 
                ON e.id_emailing = ec2.id_emailing 
                AND ec2.chave = 'num_parcela'
            WHERE ec.valor = '' OR ec.valor IS NULL
        """)
        resultado = session.execute(query)
        email_data_list = []
        for row in resultado:
            email_data = EmailData(
                id_emailing=row.id_emailing,
                destinatario_ndg=row.destinatario_ndg,
                chave_linhaDigitavel=row.chave_linhaDigitavel,
                valor_linhaDigitavel=row.valor_linhaDigitavel,
                chave_numAcordo=row.chave_numAcordo,
                valor_numAcordo=row.valor_numAcordo,
                chave_num_parcela=row.chave_num_parcela,
                valor_num_parcela=row.valor_num_parcela
            )
            email_data_list.append(email_data)
        return email_data_list

