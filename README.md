# WhatsappSenderServer

Servidor para envio de mensagens WhatsApp via Evolution API, utilizando arquitetura orientada a eventos com Kafka.

## Visão geral

Sistema completo para gerenciar envios de mensagens WhatsApp com autenticação JWT, persistência em MongoDB e processamento assíncrono via Kafka.

**Arquitetura:**

- **API REST** (FastAPI): Gerencia usuários e enfileira mensagens
- **Producer Kafka**: Publica mensagens no tópico `messages`
- **Consumer Kafka**: Consome mensagens e envia via Evolution API
- **Autenticação**: JWT com hash de senhas bcrypt
- **Banco de dados**: MongoDB para persistência de usuários

## Instalação e Execução

### Modo Docker (Recomendado)

Pré-requisitos: Docker e Docker Compose

```sh
# Configurar variáveis de ambiente
cp .env.example .env
nano .env  # Ajustar conforme necessário

# Iniciar serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f api
docker-compose logs -f consumer
```

### Modo Local

```sh
# Criar ambiente Python
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar API
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints Principais

| Método | Endpoint                  | Descrição                    |
| ------ | ------------------------- | ---------------------------- |
| POST   | `/user/signup`            | Criar novo usuário           |
| POST   | `/user/login`             | Autenticar e obter JWT       |
| POST   | `/whatsappsender/message` | Enfileirar mensagem WhatsApp |

**Exemplo de envio:**

```json
POST /whatsappsender/message
{
  "instance": "seu_numero",
  "recipient_number": "551199999999",
  "message": "Olá!"
}
```

## Fluxo de Funcionamento

1. Cliente faz requisição POST para `/whatsappsender/message`
2. API valida JWT e enfileira mensagem no Kafka (tópico `messages`)
3. Consumer lê a mensagem do Kafka
4. Envia para Evolution API via HTTP
5. Evolution API encaminha para WhatsApp

## Variáveis de Ambiente

```env
# JWT e Segurança
JWT_SECRET=sua_chave_secreta
SECRET_KEY=sua_chave_de_criptografia

# Evolution API
AUTHENTICATION_API_KEY=sua_api_key_evolution
EVOLUTION_API_URL=http://localhost:8080

# Kafka
KAFKA_PORT=9092

# MongoDB
MONGO_USERNAME=admin
MONGO_PASSWORD=senha
MONGO_URL=mongodb://localhost:27017
```

## Estrutura do Projeto

```
src/
├── main.py                 # API principal (FastAPI)
├── producer.py             # Producer Kafka
├── controller.py           # Conexão MongoDB
├── auth_handler.py         # Autenticação JWT
├── security.py             # Hash de senhas
├── models.py               # Modelos Pydantic
├── consumer/
│   ├── consumer.py         # Consumer Kafka
│   └── whatsappsender.py   # Integração Evolution API
└── requirements.txt

docker-compose.yml          # Orquestração de serviços
.env                        # Variáveis de ambiente
```

## Logs

- **API**: `logs_whatsappsenderserver.log`
- **Consumer**: `consumer.log`

Visualizar em tempo real:

```sh
docker-compose logs -f api consumer
```

## Tecnologias

- **FastAPI** - Framework web
- **Kafka** - Message broker
- **MongoDB** - Banco de dados
- **PyJWT** - Autenticação
- **Docker** - Containerização

## Contribuindo

1. Abra uma issue descrevendo a mudança
2. Envie um pull request com commits claros
3. Mantenha PRs pequenas e focadas
