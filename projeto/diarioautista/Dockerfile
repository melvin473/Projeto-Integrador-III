# Imagem oficial do Python
FROM python:3.11-slim

# Variáveis de ambiente para otimização
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev curl gcc \
    && apt-get clean

# Define o diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências e instala
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir -p /app/nltk_data
RUN python -c "import nltk; [nltk.download(pkg, download_dir='/app/nltk_data') for pkg in ['punkt', 'punkt_tab', 'averaged_perceptron_tagger', 'vader_lexicon']]"

# Copia o restante do código
COPY . .

# Corrige permissões do arquivo da chave privada (opcional)
RUN chmod 600 /app/certificados/client-key.pem || true

# Comando para rodar o servidor via Gunicorn
CMD ["gunicorn", "diarioautista.wsgi:application", "--bind", "0.0.0.0:8080"]
