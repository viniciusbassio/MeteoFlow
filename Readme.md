# 🌦️ MeteoFlow

**MeteoFlow** é um worker desenvolvido em Python responsável por consumir dados meteorológicos enviados via MQTT por uma estação baseada em ESP32 e armazená-los em um banco de dados MySQL.

O projeto faz parte de uma solução de monitoramento meteorológico IoT, permitindo a coleta contínua e o armazenamento histórico das condições ambientais.

## 🏗️ Arquitetura

```text
┌─────────────────────┐
│       ESP32         │
│ Estação Meteorológica│
└──────────┬──────────┘
           │
           │ MQTT / TLS
           ▼
┌─────────────────────┐
│    HiveMQ Cloud     │
│      MQTT Broker    │
└──────────┬──────────┘
           │
           │ weather/data
           ▼
┌─────────────────────┐
│      MeteoFlow      │
│       Python        │
└──────────┬──────────┘
           │
           │ MySQL
           ▼
┌─────────────────────┐
│       MySQL 8       │
│        VPS          │
└─────────────────────┘
```

## 📡 Dados coletados

Atualmente, a estação envia as seguintes informações:

| Campo       | Descrição                               |
| ----------- | --------------------------------------- |
| `id`        | Identificador da estação                |
| `ts`        | Data e hora da leitura                  |
| `temp_c`    | Temperatura em °C                       |
| `hum_pct`   | Umidade relativa do ar (%)              |
| `press_hpa` | Pressão atmosférica local (hPa)         |
| `press_sl`  | Pressão corrigida ao nível do mar (hPa) |
| `alt_m`     | Altitude estimada (m)                   |
| `uv_idx`    | Índice UV                               |
| `uv_raw`    | Leitura bruta do sensor UV              |
| `trend`     | Tendência da pressão atmosférica        |

Exemplo de payload:

```json
{
  "press_hpa": 965.36,
  "uv_idx": 0.0,
  "press_sl": 1010.91,
  "alt_m": 406.57,
  "uv_raw": 0.0,
  "temp_c": 24.6,
  "id": "adamantina_01",
  "ts": "2026-08-26T22:53:38",
  "hum_pct": 62,
  "trend": "estavel"
}
```

## 🛠️ Tecnologias

* Python 3
* MQTT
* HiveMQ Cloud
* MySQL 8
* `paho-mqtt`
* `mysql-connector-python`
* `python-dotenv`
* ESP32 / MicroPython

## 📁 Estrutura

```text
MeteoFlow/
├── main.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### `main.py`

Responsável por:

* conectar ao broker MQTT;
* assinar o tópico configurado;
* receber os payloads da estação;
* desserializar os dados JSON;
* encaminhar as leituras para persistência.

### `database.py`

Responsável pela conexão com o MySQL e persistência das leituras meteorológicas.

## ⚙️ Configuração

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd MeteoFlow
```

Crie um ambiente virtual:

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🔐 Variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
MYSQL_HOST=
MYSQL_PORT=3306
MYSQL_DATABASE=meteoflow
MYSQL_USER=
MYSQL_PASSWORD=

MQTT_HOST=
MQTT_PORT=8883
MQTT_USER=
MQTT_PASSWORD=
MQTT_TOPIC=weather/data
```

> O arquivo `.env` contém credenciais e não deve ser versionado.

## 🗄️ Banco de dados

O MeteoFlow utiliza atualmente a tabela `weather_readings`.

```sql
CREATE TABLE weather_readings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    estacao VARCHAR(50) NOT NULL,
    data_hora DATETIME NOT NULL,
    temperatura_c DOUBLE,
    umidade_pct DOUBLE,
    pressao_hpa DOUBLE,
    pressao_nivel_mar_hpa DOUBLE,
    altitude_m DOUBLE,
    uv_indice DOUBLE,
    uv_raw DOUBLE,
    tendencia VARCHAR(30),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_data_hora (data_hora),
    INDEX idx_estacao_data (estacao, data_hora)
);
```

## ▶️ Execução

Com o ambiente virtual ativo:

```bash
python main.py
```

Quando conectado corretamente:

```text
MeteoFlow iniciado
MQTT conectado | tópico: weather/data
Recebido: adamantina_01 | 2026-08-26T22:56:23 | 24.62 °C
Registro salvo no MySQL
```

## 🔄 Fluxo de processamento

```text
ESP32
  │
  │ JSON
  ▼
MQTT Broker
  │
  │ weather/data
  ▼
MeteoFlow
  │
  ├── Recebe mensagem
  ├── Desserializa JSON
  ├── Mapeia os dados
  └── Persiste leitura
          │
          ▼
        MySQL
```

## 🚀 Próximas melhorias

* Validação dos payloads recebidos
* Logging estruturado
* Pool de conexões MySQL
* Tratamento avançado de reconexão MQTT
* Proteção contra registros duplicados
* Monitoramento de disponibilidade da estação
* Execução como serviço `systemd`
* Suporte a múltiplas estações
* API para consulta dos dados históricos
* Dashboard para visualização meteorológica

## 📌 Status

**MVP funcional.**

O fluxo de aquisição e persistência já foi validado de ponta a ponta:

**ESP32 → HiveMQ Cloud → MeteoFlow → MySQL**

As leituras meteorológicas são recebidas via MQTT e armazenadas automaticamente no banco de dados.
