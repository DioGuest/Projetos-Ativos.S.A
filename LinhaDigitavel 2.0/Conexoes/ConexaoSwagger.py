import requests  # Importa a biblioteca requests para fazer requisições HTTP
import os  # Importa a biblioteca os para acessar variáveis de ambiente
from dotenv import load_dotenv  # Importa a função load_dotenv para carregar variáveis de ambiente a partir de um arquivo .env

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as variáveis de ambiente USERNAME_SWAGGER, PASSWORD_SWAGGER e URL_SWAGGER
username = os.getenv('USERNAME_SWAGGER')
password = os.getenv('PASSWORD_SWAGGER')
url = os.getenv('URL_SWAGGER')


def ConexaoSwagger():
    
    
    # Define os dados necessários para o login
    payload = {
        'grant_type': '',
        'username': username,
        'password': password,
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Envia uma requisição POST para o endpoint de login da API
    response = requests.post(url, data=payload, headers=headers)

    # Verifica se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Extrai o token de acesso do JSON de resposta
        access_token = response.json().get('access_token')
        print("Access Token:", access_token)
        return access_token
    else:
        # Se a requisição falhar, imprime uma mensagem de erro e retorna um erro HTTP 500
        print("Failed to log in:", response.text)
        return "Erro ao fazer login Na API", 500  # Retorna um erro HTTP 500 em caso de falha de login
    
    
