import os
import ldap3
import time
import requests

from dotenv import load_dotenv
load_dotenv()

TENANT_ID_AZURE = os.getenv('TENANT_ID_AZURE')
CLIENTE_ID_AZURE = os.getenv('CLIENTE_ID_AZURE')
CLIENTE_SECRET_AZURE = os.getenv('CLIENTE_SECRET_AZURE')
SERVER_AD = os.getenv('SERVER_AD')
BASE_AD = os.getenv('BASE_AD')
LOGIN_AD = os.getenv('LOGIN_AD')
PASSWORD_AD = os.getenv('PASSWORD_AD')
TIME_LOOP = os.getenv('TIME_LOOP')




# Função para converter logonHours para decimal
def convert_logonHours_to_decimal(logonHours):
    decimal_value = 0
    for i, byte in enumerate(logonHours):
        decimal_value += byte * (256 ** i)
    return decimal_value

# Função para revogar o token do usuário
def revoke_user_token(email):
    tenant_id = TENANT_ID_AZURE
    client_id = CLIENTE_ID_AZURE
    client_secret = CLIENTE_SECRET_AZURE

    # Obtenha um token de autenticação
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': 'https://graph.microsoft.com'
    }

    # Faça a solicitação de token
    token_response = requests.post(token_url, data=token_data)

    # Verifique o código de status da resposta
    if token_response.status_code == 200:
        # Autenticação bem-sucedida
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        print("Autenticação bem-sucedida. Token de acesso obtido.")
    else:
        # Autenticação falhou
        print("Falha na autenticação. Código de status:", token_response.status_code)
        print("Resposta:", token_response.text)
        exit()  # Encerra o script em caso de falha na autenticação

    # URL para revogar o token do usuário
    revoke_url = f'https://graph.microsoft.com/v1.0/users/{email}/revokeSignInSessions'

    # Envie a solicitação para revogar o token
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.post(revoke_url, headers=headers)

    if response.status_code == 200:
        print(f'Token do usuário {email} revogado com sucesso.')
    else:
        print(f'Erro ao revogar o token do usuário {email}. Código de status:', response.status_code)
        print("Resposta:", response.text)

while True:
    # Configurar a conexão com o Active Directory
    server = ldap3.Server(SERVER_AD)
    connection = ldap3.Connection(server, user=LOGIN_AD, password=PASSWORD_AD)

    # Fazer login no Active Directory
    if not connection.bind():
        print("Erro ao fazer login no Active Directory \n")
    else:
        print("Login bem-sucedido no Active Directory")

    # Pesquisar todos os usuários com logonHours igual a 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    search_base = BASE_AD
    search_filter = '(logonHours=\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00\\00)'
    search_attributes = ['cn', 'mail', 'logonHours', 'sAMAccountName']

    connection.search(search_base, search_filter, attributes=search_attributes)

    if len(connection.entries) > 0:
        for user_entry in connection.entries:
            user = user_entry
            email = user.mail.value if user.mail else None  # Armazene o e-mail do usuário
            print(f"Usuario com horário desativado")
            print(f"Nome do usuário: {user.cn}")
            print(f"Nome do usuário: {user.sAMAccountName}")
            print(f"Email do usuário: {email}")
            print(f"logonHours do usuário: {user.logonHours} \n")

            # Chame a função para revogar o token, passando o e-mail como argumento
            if email:
                revoke_user_token(email)
    else:
        print("Nenhum usuário com logonHours igual a 0 encontrado")

    # Encerrar a conexão com o Active Directory
    connection.unbind()

    # Aguardar 16 segundos antes de executar novamente
    time.sleep(int(TIME_LOOP))
