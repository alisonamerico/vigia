# Vigia 🌧️

**Monitoramento de riscos climáticos para Pernambuco**

> Sistema que coleta dados públicos de chuva e nível de rios em tempo real, detecta situações de risco por região e envia alertas humanizados via Telegram — 24h por dia, sem que o usuário precise fazer nada além de se cadastrar uma vez.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-5-brightgreen?logo=celery)](https://docs.celeryq.dev)
[![Kafka](https://img.shields.io/badge/Kafka-Redpanda-red?logo=apachekafka)](https://redpanda.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-minikube-blue?logo=kubernetes)](https://minikube.sigs.k8s.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

______________________________________________________________________

## O problema

Pernambuco é um dos estados brasileiros mais afetados por enchentes. A Região Metropolitana do Recife sofre com eventos graves todos os anos entre março e agosto. Em maio de 2026, a APAC manteve **alerta vermelho ativo** com riscos simultâneos nos rios Capibaribe, Jaboatão, Ipojuca, Tapacurá e outros — praticamente toda a rede hídrica da RMR.

O sistema atual avisa *que choveu muito*. O Vigia avisa *o que isso significa para você e o que fazer agora.*

| | SMS / Instagram | Vigia |
|---|---|---|
| **Como chega** | Você busca ou recebe alerta genérico | Telegram, proativo, na sua região |
| **Segmentação** | Cidade ou estado inteiro | Por bairro ou município |
| **Linguagem** | Técnica ou genérica | Português simples via LLM |
| **O que fazer** | Não informa | Orientações práticas e imediatas |
| **Nível de risco** | Muitas vezes ausente | 🟡 🟠 🔴 sempre explícito |
| **Interatividade** | Zero | Usuário pode consultar a situação atual |

______________________________________________________________________

## Como funciona

```
CEMADEN · INMET · APAC · Open-Meteo
          (coleta a cada 15 min)
                  ↓
         Celery Beat + Workers
        (analisa risco por região)
                  ↓
    Kafka — topic: weather.alert.detected
                  ↓
     ┌────────────┴─────────────┐
     ↓                          ↓
Telegram Notifier         Analytics Logger
  · busca usuários           · salva histórico
  · gera msg via LLM         · alimenta dashboard
  · envia alerta
     ↓
Usuário recebe no celular 📱
```

### Exemplo de alerta recebido

```
🔴 ALERTA — Jaboatão dos Guararapes

Risco ALTO de alagamento nos próximos 60 minutos.

Registrado 87mm de chuva nas últimas 3 horas. O Rio Jaboatão
está acima da cota de alerta e com tendência de subida.

⚠️ Recomendações:
• Evite áreas baixas e próximas ao Rio Jaboatão
• Não atravesse ruas alagadas
• Fique em local seguro e elevado
• Ligue 199 (Defesa Civil) se precisar de ajuda

📊 Fonte: CEMADEN + APAC · Atualizado há 3 min
```

______________________________________________________________________

## Stack

| Camada | Tecnologia |
|---|---|
| API | FastAPI + SQLAlchemy async + PostgreSQL + PostGIS |
| Filas | Celery 5 + Redis + Celery Beat |
| Streaming | Redpanda (Kafka-compatible) |
| Bot | python-telegram-bot 21+ |
| LLM produção | Groq API — free tier, Llama 3.3 70B |
| LLM local | Ollama — llama3.2:3b |
| Containers | Docker + Docker Compose |
| Orquestração | Kubernetes (minikube local) |
| Testes | pytest + pytest-asyncio + httpx |
| Geo | PostGIS + shapely |

______________________________________________________________________

## Fontes de dados

Todas públicas, gratuitas e sem necessidade de chave de API.

| Fonte | O que fornece | Frequência |
|---|---|---|
| **CEMADEN** | Pluviômetros em áreas de risco | 10 min |
| **INMET** | Estações meteorológicas + avisos | 1 hora |
| **APAC** | Chuvas RMR + nível de rios + alertas PE | Tempo real (scraping) |
| **Open-Meteo** | Previsão 48h (fallback) | 1 hora |

______________________________________________________________________

## Níveis de alerta

| Nível | Limiar | Ação |
|---|---|---|
| 🟢 Verde | < 30mm/3h | Sem notificação |
| 🟡 Amarelo | 30–50mm/3h | Fique atento |
| 🟠 Laranja | 50–100mm/dia | Evite áreas de risco |
| 🔴 Vermelho | > 100mm ou risco alto | Saia das áreas de risco, ligue 199 |

______________________________________________________________________

## Rodando localmente

### Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker + Docker Compose

### Setup

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/vigia-pe.git
cd vigia-pe

# Instalar dependências
uv sync

# Copiar variáveis de ambiente
cp .env.example .env

# Subir infraestrutura (PostgreSQL, Redis, Redpanda)
docker compose up -d

# Aplicar migrations
uv run alembic upgrade head

# Popular regiões de Pernambuco
uv run python scripts/seed_regions.py
```

### Rodando os serviços

```bash
# Terminal 1 — API
uv run uvicorn app.main:app --reload

# Terminal 2 — Celery Worker + Beat
uv run celery -A app.workers.celery_app worker --beat --loglevel=info

# Terminal 3 — Kafka Consumer
uv run python scripts/run_consumer.py

# Terminal 4 — Bot Telegram
uv run python scripts/run_bot.py
```

Acesse a documentação da API em `http://localhost:8000/docs`

______________________________________________________________________

## Variáveis de ambiente

```bash
# .env.example

# Banco de dados
DATABASE_URL=postgresql+asyncpg://vigia_user:vigia_pass@localhost:5432/vigia

# Redis
REDIS_URL=redis://localhost:6379/0

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Telegram
TELEGRAM_BOT_TOKEN=seu_token_aqui  # obter no @BotFather

# LLM — escolha o provider
LLM_PROVIDER=ollama                 # "ollama" (local) ou "groq" (produção)

# Ollama (desenvolvimento local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Groq (produção no Render)
GROQ_API_KEY=gsk_xxxxxxxxxxxx
```

______________________________________________________________________

## LLM — Groq em produção, Ollama local

O Vigia usa LLM para transformar dados técnicos em mensagens em português simples. A mesma interface funciona com dois providers:

**Desenvolvimento local → Ollama**

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
```

**Produção no Render → Groq API**

- Criar conta gratuita em [console.groq.com](https://console.groq.com) (sem cartão)
- Gerar API Key
- Definir `LLM_PROVIDER=groq` e `GROQ_API_KEY=...` no Render

Se a LLM estiver indisponível, o sistema cai automaticamente para mensagens template — o bot nunca para de funcionar.

______________________________________________________________________

## Preparado para WhatsApp

A arquitetura usa o padrão Strategy nos notifiers. Adicionar WhatsApp no futuro é uma mudança de uma linha:

```python
consumer = AlertConsumer(notifiers=[
    TelegramNotifier(),
    WhatsAppNotifier(api_url="..."),  # Evolution API open source
])
```

O Kafka, o Celery, a API e o banco não mudam.

______________________________________________________________________

## Testes

```bash
# Rodar todos os testes
uv run pytest

# Com cobertura
uv run pytest --cov=app --cov-report=term-missing

# Testes específicos
uv run pytest tests/test_collectors.py -v
uv run pytest tests/test_analyzers.py -v
```

______________________________________________________________________

## Estrutura do projeto

```
vigia-pe/
├── app/
│   ├── collectors/       # CEMADEN, INMET, APAC, Open-Meteo
│   ├── analyzers/        # Análise de risco e thresholds
│   ├── workers/          # Celery tasks e agendamento
│   ├── kafka/            # Producer e Consumer
│   ├── notifiers/        # Telegram, WhatsApp (futuro)
│   ├── bot/              # Handlers e comandos do bot
│   ├── routers/          # Endpoints FastAPI
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # LLM service (Groq + Ollama)
├── k8s/                  # Kubernetes manifests
├── migrations/           # Alembic
├── tests/
├── scripts/
├── data/
│   └── regions_pe.geojson
└── docker-compose.yml
```

______________________________________________________________________

## Roadmap

- [x] Documentação de produto e arquitetura
- [ ] Fase 1 — FastAPI + PostgreSQL + PostGIS
- [ ] Fase 2 — Coletores + Celery Beat
- [ ] Fase 3 — Kafka + Consumers
- [ ] Fase 4 — Bot Telegram
- [ ] Fase 5 — LLM (Groq + Ollama)
- [ ] Fase 6 — Kubernetes

______________________________________________________________________

## Motivação

Este projeto nasceu como laboratório de estudos para aprender **FastAPI, Celery, Kafka e Kubernetes** na prática — mas usando um problema real que afeta pessoas reais em Pernambuco todos os anos.

Em vez de um CRUD de tarefas, um sistema que pode salvar vidas.

______________________________________________________________________

## Contato

Alison Américo · [alisonlira@proton.me](mailto:alisonlira@proton.me) · [LinkedIn](https://linkedin.com/in/alison-americo) · [Blog](https://alra.dev)

______________________________________________________________________

## Licença

MIT — veja [LICENSE](LICENSE) para detalhes.

______________________________________________________________________

*Defesa Civil PE: 199 · APAC: [apac.pe.gov.br](https://apac.pe.gov.br) · CEMADEN: [cemaden.gov.br](https://cemaden.gov.br)*
