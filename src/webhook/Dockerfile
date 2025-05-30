FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app

# Copia o conteúdo do diretório atual para o container em /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

# Expõe a porta da API (porta padrão do FastAPI é 8000)
EXPOSE 9000

# Comando para executar oFastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--timeout-keep-alive=65"]