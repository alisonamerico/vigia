# Vigia 🌧️

### Monitoramento de riscos climáticos para Pernambuco

> **Projeto de estudo com impacto real.**
> Construído para aprender FastAPI, Celery, Kafka e Kubernetes — enquanto resolve um problema que mata pessoas todos os anos no Brasil.
>
> **Repositório:** [vigia](https://github.com/alisonamerico/vigia) no GitHub

______________________________________________________________________

## Índice

1. [O que é o projeto](#1-o-que-%C3%A9-o-projeto)
1. [O problema real que ele resolve](#2-o-problema-real-que-ele-resolve)
1. [A melhoria em relação ao sistema atual](#3-a-melhoria-em-rela%C3%A7%C3%A3o-ao-sistema-atual)
1. [Fontes de dados públicas](#4-fontes-de-dados-p%C3%BAblicas)
1. [Como o alerta chega ao usuário](#5-como-o-alerta-chega-ao-usu%C3%A1rio)
1. [Fluxo completo do sistema](#6-fluxo-completo-do-sistema)
1. [Níveis de alerta](#7-n%C3%ADveis-de-alerta)
1. [O papel da LLM — Groq (produção) e Ollama (local)](#8-o-papel-da-llm--groq-produ%C3%A7%C3%A3o-e-ollama-local)
1. [Stack tecnológica](#9-stack-tecnol%C3%B3gica)
1. [Estrutura de pastas](#10-estrutura-de-pastas)
1. [Arquitetura preparada para WhatsApp](#11-arquitetura-preparada-para-whatsapp)
1. [Fases de desenvolvimento](#12-fases-de-desenvolvimento)

______________________________________________________________________

## 1. O que é o projeto

**Vigia** é uma API de monitoramento climático e hidrológico que coleta dados públicos de chuva e nível de rios em tempo real, detecta situações de risco para cada região, e envia alertas humanizados para cidadãos cadastrados via Telegram.

O sistema roda 24 horas por dia, coletando dados a cada 10–15 minutos das principais fontes meteorológicas do Brasil. Quando detecta risco — seja por chuva acima do limiar, nível de rio subindo, ou alerta oficial emitido — publica um evento no Kafka, que aciona o bot do Telegram para avisar os moradores da região afetada.

**O usuário não precisa fazer nada.** Ele se cadastra uma vez, informa o bairro ou cidade, e passa a receber alertas automaticamente sempre que há risco na sua área.

______________________________________________________________________

## 2. O problema real que ele resolve

### O contexto de Pernambuco

Pernambuco é um dos estados brasileiros mais afetados por enchentes e alagamentos. A Região Metropolitana do Recife, que inclui cidades como Jaboatão dos Guararapes, Olinda, Caruaru e Cabo de Santo Agostinho, sofre com eventos graves todos os anos durante o período chuvoso (março a agosto).

Em maio de 2026, a APAC manteve alerta vermelho ativo para a RMR, com alertas hidrológicos nos rios Tracunhaém, Jaboatão, Tapacurá, Ipojuca, Capibaribe, Duas Unas, Sirigi, Capibaribe Mirim e no Canal de Goiana — praticamente toda a rede hídrica da região metropolitana em risco simultaneamente.

### Os problemas da comunicação atual

**1. Aviso por SMS com pop-up**
O sistema atual da Defesa Civil envia SMS com pop-up de emergência (Cell Broadcast). Funciona, mas tem limitações sérias:

- A mensagem é genérica para uma área grande — "Alerta de chuva forte para Recife" não ajuda quem mora no bairro da Várzea, longe de rios
- Não informa o nível de risco de forma clara (verde, amarelo, laranja, vermelho)
- Não diz o que fazer — evacuar? ficar em casa? qual rua evitar?
- Não considera o histórico individual — se você mora em área alta, o alerta de rio não te afeta
- Não há como perguntar ou tirar dúvidas
- Pessoas com deficiência auditiva ou visual têm dificuldade de receber ou processar

**2. Instagram e site da APAC**
A APAC publica avisos no Instagram (@apac_oficial) e no site. O problema:

- Você precisa ir ativamente buscar a informação — ninguém te notifica
- A linguagem é técnica: "Zona de Convergência Intertropical deslocou-se para norte do nordeste com Distúrbios associados"
- Não há segmentação por bairro ou rua
- Algoritmo do Instagram pode não mostrar o post urgente para você

**3. Rádio e TV**
Funciona bem para alertas extremos, mas não é em tempo real e depende do usuário estar assistindo.

______________________________________________________________________

## 3. A melhoria em relação ao sistema atual

| Aspecto | Sistema atual (SMS/Instagram) | Vigia |
|---|---|---|
| **Como chega** | Você precisa buscar (Instagram) ou recebe genérico (SMS) | Chega no Telegram, proativo, na sua região específica |
| **Segmentação** | Cidade ou estado inteiro | Por bairro ou município |
| **Linguagem** | Técnica ou genérica | Humanizada pela LLM em português simples |
| **O que fazer** | Não informa | Orienta ações práticas ("evite a Av. Norte", "não atravesse o córrego") |
| **Nível de risco** | Muitas vezes ausente | Sempre explícito: 🟡 ATENÇÃO / 🟠 ALERTA / 🔴 PERIGO |
| **Frequência** | Irregular | A cada 15 minutos de monitoramento |
| **Histórico** | Não existe | Usuário consulta via bot: `/historico` |
| **Interatividade** | Zero | Usuário pode perguntar: "qual a situação do Rio Capibaribe agora?" |
| **Acessibilidade** | SMS pode não funcionar para todos | Telegram funciona em celular básico e tem recursos de acessibilidade |
| **Múltiplos locais** | Não | Usuário cadastra trabalho, escola e casa — recebe por todos |

### O diferencial mais importante

O sistema atual avisa **que choveu muito**. O Vigia avisa **o que isso significa para você e o que fazer agora** — e essa diferença pode salvar vidas.

______________________________________________________________________

## 4. Fontes de dados públicas

Todas as fontes abaixo são gratuitas, públicas e sem necessidade de cadastro ou chave de API.

______________________________________________________________________

### 4.1 CEMADEN — Centro Nacional de Monitoramento e Alertas de Desastres Naturais

**O que é:** Órgão federal vinculado ao Ministério de Ciência e Tecnologia. Opera 24h monitorando áreas de risco em 957 municípios brasileiros, incluindo toda a RMR.

**O que fornece:**

- Dados de pluviômetros a cada **10 minutos** via WebService JSON
- Localização geográfica (lat/long) de cada pluviômetro
- Volume de chuva acumulada por intervalo de tempo

**WebService:**

```
GET http://sjc.salvar.cemaden.gov.br/resources/graficos/getPcds.json
    ?uf=PE
    &inicio=YYYY-MM-DD HH:MM:SS
    &fim=YYYY-MM-DD HH:MM:SS
```

**Formato de resposta (JSON):**

```json
{
  "tipo": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-34.9, -8.1]
  },
  "properties": {
    "codEstacao": "PE001",
    "municipio": "Recife",
    "dataHora": "2026-05-02T14:00:00Z",
    "valorMedida": 12.4,
    "unidadeMedida": "mm"
  }
}
```

**Por que é importante:** O CEMADEN tem pluviômetros instalados especificamente em áreas de risco. Um valor alto aqui é sinal confiável de perigo iminente.

______________________________________________________________________

### 4.2 INMET — Instituto Nacional de Meteorologia

**O que é:** Órgão federal com mais de 570 estações meteorológicas automáticas em todo o Brasil. Atualiza dados **a cada hora**.

**O que fornece:**

- Precipitação acumulada por hora
- Temperatura, umidade, pressão, vento
- Avisos meteorológicos especiais com nível de severidade

**Endpoints principais:**

```
# Dados de uma estação específica (ex: A301 = Recife)
GET https://apitempo.inmet.gov.br/estacao/{data_inicio}/{data_fim}/{codigo_estacao}

# Lista de todas as estações por estado
GET https://apitempo.inmet.gov.br/estacoes/{tipo}
# tipo: T (todas), A (automáticas), M (manuais)

# Avisos meteorológicos ativos
GET https://apitempo.inmet.gov.br/avisos
```

**Estações relevantes para PE:**

- A301 — Recife
- A319 — Caruaru
- A349 — Petrolina
- A380 — Garanhuns

**Nota:** Existe a biblioteca Python `inmetpy` que encapsula esses endpoints e facilita o uso.

______________________________________________________________________

### 4.3 APAC — Agência Pernambucana de Águas e Clima

**O que é:** Agência estadual específica de Pernambuco. É a fonte mais relevante para o projeto por ter granularidade na RMR e no interior do estado.

**O que fornece:**

- Monitoramento de chuvas em tempo real por pluviômetro na RMR
- Avisos meteorológicos em 3 níveis: Amarelo (30–50mm/3h), Laranja (50–100mm/dia), Vermelho (>100mm)
- Monitoramento de nível de rios (Capibaribe, Ipojuca, Jaboatão e outros)
- Previsão do tempo por mesorregião

**Como coletar:** A APAC não tem API REST pública documentada, mas publica dados no site e no Instagram. A estratégia é:

1. **Scraping do site** `apac.pe.gov.br/monitoramento` — coleta dados dos pluviômetros da RMR
1. **Monitoramento do Instagram** `@apac_oficial` via scraping de posts — captura avisos de alerta publicados
1. Futuramente: contato direto com a APAC para acesso formal ao WebService interno

______________________________________________________________________

### 4.4 Open-Meteo (fallback gratuito)

**O que é:** API meteorológica open source, sem chave de API, sem limite de uso, com dados de modelos globais (GFS, ECMWF).

**Por que usar:** Serve como fallback caso o INMET ou CEMADEN estejam instáveis. Também fornece previsão para as próximas 48 horas, que o CEMADEN não oferece.

```
GET https://api.open-meteo.com/v1/forecast
    ?latitude=-8.05
    &longitude=-34.9
    &hourly=precipitation,precipitation_probability
    &forecast_days=2
    &timezone=America/Recife
```

______________________________________________________________________

### 4.5 Resumo das fontes

| Fonte | Granularidade | Frequência | Tipo de dado | Acesso |
|---|---|---|---|---|
| CEMADEN | Pluviômetro (bairro) | 10 min | Chuva observada | WebService JSON público |
| INMET | Estação (cidade) | 1 hora | Chuva + meteorologia | API REST pública |
| APAC | Pluviômetro RMR + rios | Tempo real | Chuva + nível rios + avisos | Scraping + futuro WS |
| Open-Meteo | Município | 1 hora | Previsão 48h | API REST aberta |

______________________________________________________________________

## 5. Como o alerta chega ao usuário

### Telegram Bot

O Telegram é o canal principal por ser:

- **Gratuito** — sem custo por mensagem, sem limite de usuários
- **API aberta** — `python-telegram-bot` é uma biblioteca Python madura e bem documentada
- **Democrático** — funciona em celular básico, 3G, sem internet rápida
- **Interativo** — permite comandos, botões, respostas, consultas
- **Preparado para escala** — suporta bots com milhões de usuários

### Fluxo de cadastro do usuário

```
Usuário abre Telegram → busca @VigiaBot → manda /start

Bot: "Olá! Sou o VigiaBot 🌧️
      Vou te avisar quando houver risco de enchente ou alagamento na sua região.
      Qual é a sua cidade?"

Usuário: "Jaboatão dos Guararapes"

Bot: "Perfeito! E qual é o seu bairro? (opcional, mas melhora a precisão dos alertas)"

Usuário: "Curado"

Bot: "✅ Cadastrado! Você receberá alertas para:
      📍 Jaboatão dos Guararapes — Curado
      
      Comandos disponíveis:
      /situacao — situação atual da sua região
      /rios — nível dos rios próximos
      /historico — últimos 7 dias de alertas
      /adicionar — adicionar outro local (ex: trabalho)
      /pausar — pausar alertas temporariamente"
```

### Exemplo de mensagem de alerta recebida

```
🔴 ALERTA — Jaboatão dos Guararapes

Risco ALTO de alagamento nos próximos 60 minutos.

Registrado 87mm de chuva nas últimas 3 horas em postos
próximos ao seu bairro — muito acima do limite de atenção (50mm).

O Rio Jaboatão está 0,8m acima da cota de atenção
e com tendência de subida.

⚠️ Recomendações:
• Evite áreas baixas e próximas ao Rio Jaboatão
• Não tente atravessar ruas alagadas de carro ou a pé
• Fique em local seguro e elevado
• Ligue 199 (Defesa Civil) se precisar de ajuda

📊 Fonte: CEMADEN + APAC · Atualizado há 3 min
```

______________________________________________________________________

## 6. Fluxo completo do sistema

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FONTES DE DADOS PÚBLICAS                           │
│  CEMADEN (10min)  │  INMET (1h)  │  APAC (scraping)  │  Open-Meteo  │
└──────────┬────────┴──────┬───────┴────────┬──────────┴──────┬───────┘
           │               │                │                  │
           └───────────────┴────────────────┴──────────────────┘
                                    │
                                    ▼ (a cada 15 minutos)
┌──────────────────────────────────────────────────────────────────────┐
│                    CELERY BEAT (Agendador)                            │
│  Task: collect_weather_data()                                         │
│  → Chama todas as fontes em paralelo                                  │
│  → Normaliza os dados para formato interno                            │
│  → Salva leitura raw no PostgreSQL                                    │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    CELERY WORKER (Análise)                            │
│  Task: analyze_risk()                                                 │
│  → Carrega thresholds por região (tabela no banco)                    │
│  → Compara leitura atual com limites APAC:                            │
│     Verde:   < 30mm/3h                                                │
│     Amarelo: 30–50mm/3h  ou previsão de risco baixo                  │
│     Laranja: 50–100mm/dia ou risco moderado                           │
│     Vermelho: > 100mm    ou risco alto/muito alto                     │
│  → Se nível mudou: publica evento no Kafka                            │
│  → Se nível igual ao anterior: ignora (evita spam)                    │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                 KAFKA TOPIC: weather.alert.detected                   │
│  Mensagem: {                                                          │
│    region: "Jaboatão dos Guararapes",                                 │
│    level: "RED",                                                      │
│    rain_mm: 87.3,                                                     │
│    river: "Rio Jaboatão",                                             │
│    river_level_m: 4.2,                                                │
│    sources: ["CEMADEN", "APAC"],                                      │
│    timestamp: "2026-05-02T14:00:00-03:00"                            │
│  }                                                                    │
└──────────┬───────────────────────────────────────────────────────────┘
           │
           ├─────────────────────────────────────────┐
           │                                          │
           ▼                                          ▼
┌──────────────────────┐                  ┌──────────────────────────┐
│  CONSUMER A          │                  │  CONSUMER B              │
│  Telegram Notifier   │                  │  Analytics Logger        │
│                      │                  │                          │
│  1. Busca usuários   │                  │  Salva evento no banco   │
│     cadastrados na   │                  │  para histórico e        │
│     região afetada   │                  │  dashboards futuros      │
│  2. Chama Ollama     │                  └──────────────────────────┘
│     para gerar       │
│     mensagem humana  │                  ┌──────────────────────────┐
│  3. Envia via API    │                  │  CONSUMER C (futuro)     │
│     Telegram Bot     │                  │  WhatsApp Notifier       │
└──────────────────────┘                  │  (Evolution API)         │
                                          └──────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    USUÁRIO NO TELEGRAM                                │
│  Recebe notificação no celular com:                                   │
│  • Nível de risco claro (🔴 ALERTA)                                   │
│  • Explicação em linguagem simples                                    │
│  • Recomendações práticas                                             │
│  • Fonte e horário da informação                                      │
└──────────────────────────────────────────────────────────────────────┘
```

______________________________________________________________________

## 7. Níveis de alerta

O sistema adota os mesmos níveis da APAC, para consistência com os órgãos oficiais:

| Nível | Emoji | Limiar de chuva | O que significa | Ação recomendada |
|---|---|---|---|---|
| **VERDE** | 🟢 | < 30mm/3h | Sem risco significativo | Nenhuma — sem notificação |
| **AMARELO** | 🟡 | 30–50mm/3h | Atenção: chuva significativa | Fique atento, evite áreas de risco |
| **LARANJA** | 🟠 | 50–100mm/dia | Alerta: chuva intensa | Evite áreas baixas, não atravesse ruas alagadas |
| **VERMELHO** | 🔴 | > 100mm ou risco alto | Perigo: enchente iminente | Saia de áreas de risco, ligue 199 |

**Regras anti-spam:**

- Notificação enviada apenas quando o nível **muda** (de VERDE para AMARELO, de AMARELO para LARANJA, etc.)
- Nenhuma notificação em nível VERDE — não perturbe o usuário sem necessidade
- Máximo de 1 notificação por hora por região, mesmo que os dados mudem
- Notificação de "normalização" quando o risco volta ao nível VERDE após AMARELO ou acima

______________________________________________________________________

## 8. O papel da LLM — Groq (produção) e Ollama (local)

O Vigia usa LLM para transformar dados técnicos em mensagens humanizadas em português. A arquitetura suporta dois providers com a mesma interface — você troca uma linha de configuração para alternar entre eles.

### Por que dois providers?

| Cenário | Provider | Motivo |
|---|---|---|
| **Desenvolvimento local** | Ollama | Roda na sua máquina, zero custo, zero internet |
| **Produção no Render** | Groq API | Roda na nuvem, free tier generoso, sem cartão obrigatório |

O Ollama não consegue ser chamado pelo Render — são ambientes separados. Para produção, o Groq é a solução natural: API compatível com OpenAI SDK, modelos Llama 3 e Mixtral disponíveis gratuitamente, latência muito baixa.

### Groq API — setup

```bash
# Criar conta em console.groq.com (gratuito, sem cartão)
# Gerar API Key no painel
# Adicionar no .env:
GROQ_API_KEY=gsk_xxxxxxxxxxxx
LLM_PROVIDER=groq   # ou "ollama" para desenvolvimento local
```

```python
# app/services/llm_service.py
import httpx
from app.config import settings


class LLMService:
    """
    Cliente unificado para LLM.
    Alterna entre Groq (produção) e Ollama (local)
    via variável de ambiente LLM_PROVIDER.
    """

    async def generate_alert_message(self, event: dict) -> str:
        if settings.LLM_PROVIDER == "groq":
            return await self._call_groq(event)
        return await self._call_ollama(event)

    async def _call_groq(self, event: dict) -> str:
        prompt = self._build_prompt(event)
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",  # gratuito no free tier
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

    async def _call_ollama(self, event: dict) -> str:
        prompt = self._build_prompt(event)
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 300},
                },
            )
            response.raise_for_status()
            return response.json()["response"].strip()

    def _build_prompt(self, event: dict) -> str:
        """Prompt compartilhado entre Groq e Ollama."""
        return f"""Você é o Vigia, sistema de alertas climáticos de Pernambuco.
Gere uma mensagem de alerta clara, humana e em português brasileiro simples.
Máximo 5 linhas. Inclua o nível de risco, o que está acontecendo e o que a pessoa deve fazer.

Dados do alerta:
- Região: {event['region']}
- Nível: {event['level']}
- Chuva acumulada (3h): {event.get('rain_mm', 'N/A')}mm
- Rio: {event.get('river', 'N/A')}
- Situação do rio: {event.get('river_status', 'N/A')}
- Tendência: {event.get('tendency', 'N/A')}

Responda apenas com a mensagem de alerta, sem explicações adicionais."""


llm_service = LLMService()
```

### Variáveis de ambiente por ambiente

```bash
# .env (desenvolvimento local)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# .env.render (produção)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxxxxxxxxx
```

### Fallback seguro

Se a LLM falhar (timeout, rate limit, indisponibilidade), o sistema não para — cai para uma mensagem template pré-definida e registra o erro:

```python
async def generate_alert_message(self, event: dict) -> str:
    try:
        return await self._call_provider(event)
    except Exception as e:
        logger.error(f"LLM indisponível: {e} — usando template")
        return self._fallback_template(event)

def _fallback_template(self, event: dict) -> str:
    emoji = {"GREEN": "🟢", "YELLOW": "🟡", "ORANGE": "🟠", "RED": "🔴"}
    return (
        f"{emoji.get(event['level'], '⚠️')} ALERTA — {event['region']}\n\n"
        f"Risco climático detectado na sua região.\n"
        f"Chuva acumulada: {event.get('rain_mm', 'N/A')}mm\n\n"
        f"Fique atento e siga as orientações da Defesa Civil.\n"
        f"📞 199"
    )
```

### O que a LLM faz no Vigia

**1. Humanizar o alerta**

Entrada (dados técnicos):

```json
{
  "region": "Jaboatão dos Guararapes",
  "level": "RED",
  "rain_mm_3h": 87.3,
  "river": "Rio Jaboatão",
  "river_above_quota_m": 0.8,
  "tendency": "subindo"
}
```

Saída (mensagem para o usuário):

```
🔴 ALERTA — Jaboatão dos Guararapes

Risco ALTO de alagamento nos próximos 60 minutos.

Registrado 87mm de chuva nas últimas 3 horas — muito acima do
limite de atenção. O Rio Jaboatão está subindo e já ultrapassou
a cota de alerta em quase 1 metro.

⚠️ Recomendações:
• Evite áreas baixas e próximas ao Rio Jaboatão
• Não atravesse ruas alagadas
• Fique em local seguro e elevado
• Ligue 199 (Defesa Civil) se precisar de evacuação
```

**2. Responder perguntas do usuário via bot**

Usuário: "O Capibaribe vai transbordar hoje?"

LLM recebe: dados atuais do rio + histórico + previsão Open-Meteo para as próximas 6h e responde em linguagem natural.

**3. Resumo diário às 7h**

Todo dia o sistema envia um resumo do dia anterior e a previsão para o dia — gerado pela LLM com base nos dados coletados.

______________________________________________________________________

## 9. Stack tecnológica

```
Linguagem:        Python 3.12
Gerenciador:      uv
API Framework:    FastAPI 0.115+
ORM:              SQLAlchemy 2.0 async + Alembic
Banco de dados:   PostgreSQL 16 com extensão PostGIS
                  (geoespacial — armazena polígonos de regiões de risco)
Cache:            Redis 7
Task Queue:       Celery 5 + Celery Beat (agendamento)
Streaming:        Redpanda (Kafka-compatible, leve para local)
Bot Telegram:     python-telegram-bot 21+
LLM produção:     Groq API — free tier, Llama 3.3 70B, sem cartão
LLM local:        Ollama (llama3.2:3b ou mistral:7b) — desenvolvimento
HTTP Client:      httpx (async)
Scraping:         httpx + BeautifulSoup4
Containers:       Docker + Docker Compose
Orquestração:     minikube (Kubernetes local)
Testes:           pytest + pytest-asyncio + httpx
Geo:              shapely + geopy (verificar se ponto está em polígono de risco)
```

### Por que PostGIS?

Você já tem experiência com PostGIS no projeto da SOSMA. Aqui ele serve para armazenar polígonos de bairros e áreas de risco, e verificar se um usuário cadastrado em (lat, long) está dentro de uma região afetada por um alerta.

```sql
-- Exemplo: usuários dentro de uma área de alerta
SELECT u.telegram_id, u.nome
FROM usuarios u
JOIN regioes_risco r ON ST_Contains(r.geom, u.location::geometry)
WHERE r.nivel_alerta = 'RED';
```

______________________________________________________________________

## 10. Estrutura de pastas

```
alagabot/
├── app/
│   ├── main.py                        # FastAPI app
│   ├── config.py                      # Settings (pydantic-settings)
│   ├── database.py                    # SQLAlchemy async + PostGIS
│   │
│   ├── models/
│   │   ├── alert.py                   # Model de alertas gerados
│   │   ├── region.py                  # Regiões monitoradas + geometria
│   │   ├── reading.py                 # Leituras brutas das fontes
│   │   └── user.py                    # Usuários cadastrados no bot
│   │
│   ├── schemas/
│   │   ├── alert.py                   # Pydantic schemas de alertas
│   │   └── user.py                    # Schemas de usuário/cadastro
│   │
│   ├── routers/
│   │   ├── alerts.py                  # GET /alerts, GET /alerts/{region}
│   │   ├── regions.py                 # GET /regions (regiões monitoradas)
│   │   └── health.py                  # GET /health
│   │
│   ├── collectors/                    # Coletores de dados externos
│   │   ├── base.py                    # Classe base para coletores
│   │   ├── cemaden.py                 # Coleta do WebService CEMADEN
│   │   ├── inmet.py                   # Coleta da API INMET
│   │   ├── apac.py                    # Scraping da APAC
│   │   └── open_meteo.py              # Fallback Open-Meteo
│   │
│   ├── analyzers/
│   │   ├── risk_analyzer.py           # Compara leituras com thresholds
│   │   └── thresholds.py             # Configuração de limiares por região
│   │
│   ├── workers/
│   │   ├── celery_app.py              # Config Celery + Beat schedule
│   │   ├── collect_task.py            # Task: coletar dados de todas as fontes
│   │   └── analyze_task.py            # Task: analisar risco e emitir alerta
│   │
│   ├── kafka/
│   │   ├── producer.py                # Publica eventos de alerta
│   │   └── consumer.py               # Consume e despacha para handlers
│   │
│   ├── notifiers/                     # Canais de notificação (plugáveis)
│   │   ├── base.py                    # Interface base (padrão Strategy)
│   │   ├── telegram_notifier.py       # Implementação Telegram
│   │   └── whatsapp_notifier.py       # Implementação WhatsApp (futuro)
│   │
│   ├── bot/                           # Lógica do bot Telegram
│   │   ├── handlers.py                # Handlers de comandos (/start, /situacao)
│   │   ├── keyboards.py               # Botões inline do Telegram
│   │   └── bot_runner.py              # Inicialização do bot
│   │
│   └── services/
│       └── llm_service.py             # Client LLM unificado (Groq + Ollama)
│
├── migrations/                        # Alembic
├── tests/
│   ├── conftest.py
│   ├── test_collectors.py
│   ├── test_analyzers.py
│   ├── test_alerts_api.py
│   └── test_bot_handlers.py
│
├── k8s/                               # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── postgres/
│   ├── redis/
│   ├── redpanda/
│   ├── api/
│   ├── worker/
│   └── bot/
│
├── scripts/
│   ├── run_consumer.py                # Inicia consumer Kafka
│   ├── run_bot.py                     # Inicia bot Telegram
│   └── seed_regions.py               # Popula regiões de risco iniciais
│
├── data/
│   └── regions_pe.geojson             # GeoJSON das regiões de risco de PE
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

______________________________________________________________________

## 11. Arquitetura preparada para WhatsApp

A estrutura foi desenhada para que adicionar WhatsApp no futuro seja uma mudança mínima — sem reescrever o core do sistema.

### Padrão Strategy nos Notifiers

```python
# app/notifiers/base.py
from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    """
    Interface comum para todos os canais de notificação.
    Qualquer novo canal (WhatsApp, Email, SMS) implementa esta interface.
    """
    
    @abstractmethod
    async def send_alert(self, user_id: str, message: str, level: str) -> bool:
        """Envia alerta para um usuário. Retorna True se enviado com sucesso."""
        ...

    @abstractmethod
    async def send_message(self, user_id: str, text: str) -> bool:
        """Envia mensagem genérica."""
        ...
```

```python
# app/notifiers/telegram_notifier.py
from app.notifiers.base import BaseNotifier

class TelegramNotifier(BaseNotifier):
    async def send_alert(self, user_id: str, message: str, level: str) -> bool:
        # Implementação Telegram
        ...

# app/notifiers/whatsapp_notifier.py  ← criado quando necessário
class WhatsAppNotifier(BaseNotifier):
    async def send_alert(self, user_id: str, message: str, level: str) -> bool:
        # Implementação Evolution API (WhatsApp open source)
        ...
```

### Consumer Kafka com múltiplos notifiers

```python
# app/kafka/consumer.py
class AlertConsumer:
    def __init__(self, notifiers: list[BaseNotifier]):
        self.notifiers = notifiers  # lista de canais ativos

    async def handle_alert(self, event: dict):
        users = await self.get_users_in_region(event["region"])
        message = await llm_service.generate_alert_message(event)
        
        for user in users:
            for notifier in self.notifiers:
                # cada notifier tenta enviar
                # se o usuário usa Telegram → TelegramNotifier envia
                # se usa WhatsApp → WhatsAppNotifier envia
                if notifier.supports(user.channel):
                    await notifier.send_alert(user.channel_id, message, event["level"])
```

### Adicionar WhatsApp no futuro

```python
# Apenas criar o arquivo whatsapp_notifier.py e registrar no consumer:
consumer = AlertConsumer(notifiers=[
    TelegramNotifier(),
    WhatsAppNotifier(api_url="http://localhost:8080"),  # Evolution API local
])
```

**Nenhum outro arquivo muda.** O Kafka, o Celery, a API, o banco — tudo permanece idêntico.

### Evolution API (WhatsApp open source)

Quando chegar a hora de adicionar WhatsApp:

```bash
# Evolution API roda via Docker, local, sem custo
docker run -d \
  -p 8080:8080 \
  -e AUTHENTICATION_API_KEY=minha-chave \
  atendai/evolution-api:latest
```

A Evolution API simula o WhatsApp Business sem as restrições e custos da API oficial. Perfeita para estudos e projetos de impacto social.

______________________________________________________________________

## 12. Fases de desenvolvimento

### Fase 1 — FastAPI + PostgreSQL + PostGIS (2 semanas)

- Setup do projeto com uv
- Docker Compose com PostgreSQL + PostGIS + Redis
- Models: Region, Reading, Alert, User
- Migrations com Alembic
- Endpoints REST: `GET /alerts`, `GET /regions`, `GET /health`
- Seed das regiões de Pernambuco via GeoJSON
- Testes com pytest + httpx

### Fase 2 — Coletores + Celery Beat (2 semanas)

- Coletor CEMADEN (WebService JSON)
- Coletor INMET (API REST)
- Coletor APAC (scraping)
- Coletor Open-Meteo (fallback)
- Celery Beat: coleta a cada 15 minutos
- Analisador de risco com thresholds por região
- Testes com mocks das APIs externas

### Fase 3 — Kafka + Consumers (2 semanas)

- Redpanda via Docker Compose
- Producer: publica evento quando nível de alerta muda
- Consumer A: Telegram Notifier
- Consumer B: Analytics Logger
- Lógica anti-spam (cooldown por região)
- Testes de integração do fluxo completo

### Fase 4 — Bot Telegram (1–2 semanas)

- Criação do bot no @BotFather
- Handlers: `/start`, `/situacao`, `/rios`, `/historico`, `/adicionar`
- Cadastro de usuários com localização (cidade + bairro)
- Botões inline para facilitar navegação
- Testes do bot com modo polling

### Fase 5 — LLM: Groq (produção) + Ollama (local) (1 semana)

- Criar `llm_service.py` com interface unificada
- Configurar Groq API no Render (free tier, sem cartão)
- Configurar Ollama local para desenvolvimento
- Fallback para template quando LLM indisponível
- Geração de mensagens humanizadas de alerta
- Resposta a perguntas livres do usuário no bot
- Geração de resumo diário às 7h

### Fase 6 — Kubernetes (2 semanas)

- Dockerfile otimizado
- Manifests K8s: API, Worker, Consumer, Bot
- ConfigMap + Secrets
- Probes de liveness e readiness
- Horizontal Pod Autoscaler no worker
- Rolling updates sem downtime

______________________________________________________________________

## Referências

- CEMADEN WebService: `http://sjc.salvar.cemaden.gov.br/resources/graficos/`
- INMET API: `https://apitempo.inmet.gov.br/`
- APAC: `https://www.apac.pe.gov.br/`
- Open-Meteo: `https://open-meteo.com/`
- python-telegram-bot: `https://python-telegram-bot.org/`
- Evolution API (WhatsApp): `https://github.com/EvolutionAPI/evolution-api`
- inmetpy (wrapper Python): `https://pypi.org/project/inmetpy/`
- Groq API (LLM produção): `https://console.groq.com/`
- Ollama (LLM local): `https://ollama.com/`
- Defesa Civil PE: `https://www.defesacivil.pe.gov.br/` (fone: 199)

______________________________________________________________________

*Documento de produto e arquitetura do **Vigia** — gerado como base para desenvolvimento.*
*Repositório: [vigia](https://github.com/alisonamerico/vigia) · Cada fase está detalhada o suficiente para ser executada por um agente de desenvolvimento com contexto completo.*
