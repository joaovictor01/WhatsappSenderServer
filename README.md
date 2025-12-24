# WhatsappSenderServer

Servidor API e serviços auxiliares para envio de mensagens WhatsApp via Evolution API e Kafka.

## Visão geral

Projeto composto por:

- API principal (FastAPI) para cadastro, autenticação e enfileiramento de mensagens.
  - Código: [src/main.py](src/main.py) — funções principais: [`main.create_user`](src/main.py), [`main.user_login`](src/main.py), [`main.send_message`](src/main.py).
- Producer Kafka usado pela API: [`producer.kafka_producer`](src/producer.py) — [src/producer.py](src/producer.py).
- Consumer que consome tópicos Kafka e encaminha para Evolution API:
  - Consumidor principal: [`consumer.consumer`](src/consumer/consumer.py) — [src/consumer/consumer.py](src/consumer/consumer.py).
  - Envio via Evolution API: [`consumer.whatsappsender.send_message`](src/consumer/whatsappsender.py) — [src/consumer/whatsappsender.py](src/consumer/whatsappsender.py).
- Webhook simples para receber eventos e publicar no Kafka:
  - App: [`webhook.webhook`](src/webhook/webhook.py) — [src/webhook/webhook.py](src/webhook/webhook.py).
  - Producer local: [`webhook.producer.kafka_producer`](src/webhook/producer.py) — [src/webhook/producer.py](src/webhook/producer.py).
- Autenticação/JWT: [`auth_handler.sign_jwt`](src/auth_handler.py), [`auth_handler.decode_jwt`](src/auth_handler.py), [`auth_handler.JWTBearer`](src/auth_handler.py) — [src/auth_handler.py](src/auth_handler.py).
- Segurança de senhas e criptografia: [`security.hash_password`](src/security.py), [`security.verify_password`](src/security.py) — [src/security.py](src/security.py).
- Persistência Mongo (helper): [`controller.get_db`](src/controller.py), [`controller.insert_user`](src/controller.py) — [src/controller.py](src/controller.py).
- Modelos Pydantic: [src/models.py](src/models.py) — [`models.UserSchema`](src/models.py), [`models.WhatsappMessage`](src/models.py).

Arquivos de configuração/infra:

- Orquestração: [docker-compose.yml](docker-compose.yml)
- Variáveis de ambiente: [.env](.env)
- Imagens Docker por serviço: [src/Dockerfile](src/Dockerfile), [src/consumer/Dockerfile](src/consumer/Dockerfile), [src/webhook/Dockerfile](src/webhook/Dockerfile)
- Exemplo de criação de instância Evolution: [instance_create.json](instance_create.json)

## Instalando / Executando (modo recomendado)

Pré-requisito: Docker e Docker Compose.

1. Ajuste variáveis em [.env](.env).
2. Levante os serviços:

```sh
docker-compose up -d
```

3. Logs:

- API: logs no container `api_whatsappsenderserver` e arquivo `logs_whatsappsenderserver.log` ([src/controller.py](src/controller.py)).
- Consumer: `consumer.log` ([src/consumer/consumer.py](src/consumer/consumer.py)).
- Webhook: `webhook.log` ([src/webhook/webhook.py](src/webhook/webhook.py)).

## Endpoints principais

- POST /user/signup — implementação: [`main.create_user`](src/main.py) ([src/main.py](src/main.py))
- POST /user/login — implementação: [`main.user_login`](src/main.py) ([src/main.py](src/main.py))
- POST /whatsappsender/message — enfileira mensagem via Kafka (`topic: messages`), implementação: [`main.send_message`](src/main.py) ([src/main.py](src/main.py))
- Webhook (opcional): POST /webhook ([src/webhook/webhook.py](src/webhook/webhook.py))

Observações:

- Producer Kafka usado pela API: [`producer.kafka_producer`](src/producer.py).
- Consumer consome tópicos `messages` e `webhook` ([src/consumer/consumer.py](src/consumer/consumer.py)).

## Variáveis de ambiente importantes

Variáveis de ambiente [.env](.env). Principais:

- JWT_SECRET — usado em [`auth_handler`](src/auth_handler.py)
- SECRET_KEY — usado em [`security`](src/security.py)
- AUTHENTICATION_API_KEY — usado por [`consumer.whatsappsender.send_message`](src/consumer/whatsappsender.py)
- MONGO_USERNAME / MONGO_PASSWORD — usados por Mongo / mongo-express

## Desenvolvimento local

Se preferir executar local (sem Docker):

1. Crie e ative um virtualenv.
2. Instale dependências: `pip install -r requirements.txt` ([requirements.txt](requirements.txt)).
3. Execute a API:

```sh
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Estrutura do repositório

```
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
└── src
    ├── Dockerfile
    ├── auth_handler.py
    ├── consumer
    │   ├── Dockerfile
    │   ├── __init__.py
    │   ├── consumer.py
    │   ├── requirements.txt
    │   └── whatsappsender.py
    ├── controller.py
    ├── main.py
    ├── models.py
    ├── producer.py
    ├── requirements.txt
    └── security.py
```

- src/ — código da API, producer, consumer e webhook ([src/](src))
- docker-compose.yml — orquestração local
- .env — variáveis de ambiente
- instance_create.json — exemplo payload Evolution API

## Contribuindo

- Abrir issue descrevendo bug/feature.
- PRs pequenas e focadas.
