"""
Este módulo contém funções para processar e fazer requisições para a API de boleto.
"""

import os
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor


from Conexoes.ConexaoSwagger import ConexaoSwagger
from Operacao_DB.Update_linha_digitave import update_linha_digitavel


load_dotenv()
# Variáveis de ambiente
URL_SWAGGER_REQUEST = os.getenv('URL_SWAGGER_REQUEST')



def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """
    Cria uma sessão de requisição com retry automático.
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def process_and_request_api(engine, email_data_list):
    """
    Processa e faz requisições para a API de boleto.
    """
    api_responses = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for email_data in email_data_list:
            if email_data.destinatario_ndg and email_data.valor_numAcordo and email_data.valor_num_parcela:
                url = f'{URL_SWAGGER_REQUEST}{email_data.destinatario_ndg}/{email_data.valor_numAcordo}/{email_data.valor_num_parcela}'
                futures.append(executor.submit(request_and_process, url, engine, email_data.id_emailing, api_responses))
            else:
                print(f"Algumas informações estão faltando para construir a URL do boleto para id_emailing: {email_data.id_emailing}")
        
        for future in futures:
            future.result()

    return api_responses



def request_and_process(url, engine, id_emailing, api_responses):
    """
    Faz uma requisição e processa a resposta da API de boleto.
    """
    access_token = ConexaoSwagger()
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'accept': 'application/json',
        }
        try:
            with requests_retry_session() as session:
                response = session.get(url, headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    api_responses.append(response_data)
                    linha_digitavel = response_data.get('linha_digitavel')
                    if linha_digitavel:
                        update_linha_digitavel(engine, id_emailing, linha_digitavel)
                else:
                    print(f"Falha na requisição para URL: {url} - Código de status: {response.status_code}")
        except requests.RequestException as e:
            print(f"Erro na requisição para URL: {url} - Erro: {e}")



