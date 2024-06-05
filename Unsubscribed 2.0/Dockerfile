# Use a imagem oficial do Python
FROM python:3.11.9

# Instale as dependências necessárias
RUN apt-get update && apt-get install -y apt-transport-https curl gnupg2

# Adicione o repositório do Microsoft ODBC ao seu sistema
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update

# Instale o pacote msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Instale as dependências do Python
RUN apt-get install -y python3-dev unixodbc-dev

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt && pip install --user pyodbc

# Copie o código-fonte do projeto para o diretório de trabalho
COPY . /app

# Defina a porta na qual o aplicativo Flask será executado
EXPOSE 5000

# Inicie o aplicativo Flask
CMD ["python3.11", "main.py"]
