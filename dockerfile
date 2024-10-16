# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Defina o diretório de trabalho na imagem
WORKDIR /app

# Copie os arquivos de requisitos para a imagem
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para a imagem
COPY ./app /app

# Exponha a porta que a aplicação usará
EXPOSE 8000

# Comando para rodar a aplicação usando uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
