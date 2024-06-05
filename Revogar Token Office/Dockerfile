# Use uma imagem Python como base
FROM python:3.10

# Copie o script para o diretório de trabalho do contêiner
COPY Revogar_Token_Office.py /app/Revogar_Token_Office.py

# Instale as dependências do script
RUN pip install ldap3 requests

# Defina o diretório de trabalho
WORKDIR /app

# Comando padrão para executar o script
CMD ["python", "script.py"]
