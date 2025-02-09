FROM python:3.12.9

# Instala dependências do sistema, incluindo o FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expõe a porta que a Railway usará (geralmente 8080)
EXPOSE 8080

# Comando para iniciar a aplicação com Gunicorn, chamando a função app_main
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app_main"]
