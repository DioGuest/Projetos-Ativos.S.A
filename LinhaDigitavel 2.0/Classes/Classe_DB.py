"""
    Classe que representa os dados de um emailing no banco de dados.
    
    Atributos:
    - id_emailing: identificador do emailing no banco de dados
    - destinatario_ndg: número de identificação do destinatário (NDG)
    - chave_linhaDigitavel: chave da linha digitável
    - valor_linhaDigitavel: valor da linha digitável
    - chave_numAcordo: chave do número do acordo
    - valor_numAcordo: valor do número do acordo
    - chave_num_parcela: chave do número da parcela
    - valor_num_parcela: valor do número da parcela
    """
class EmailData:
    def __init__(self, id_emailing, destinatario_ndg, chave_linhaDigitavel, valor_linhaDigitavel, chave_numAcordo, valor_numAcordo, chave_num_parcela, valor_num_parcela):
        self.id_emailing = id_emailing
        self.destinatario_ndg = destinatario_ndg
        self.chave_linhaDigitavel = chave_linhaDigitavel
        self.valor_linhaDigitavel = valor_linhaDigitavel
        self.chave_numAcordo = chave_numAcordo
        self.valor_numAcordo = valor_numAcordo
        self.chave_num_parcela = chave_num_parcela
        self.valor_num_parcela = valor_num_parcela
    
