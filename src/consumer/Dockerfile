FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app

# Copia o conteúdo do diretório atual para o container em /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv


CMD ["python", "consumer.py"]
