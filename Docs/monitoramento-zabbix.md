# Monitoramento de Integridade dos Backups (Observabilidade)

## 1. Objetivo
Não basta apenas usar o Zabbix para alimentar o inventário do Oxidized; é critico monitorar se o **Oxidized está operando corretamente**.
Este documento descreve como configurar o Zabbix para consumir a API REST do Oxidized e alertar proativamente caso falhas ocorram.

## 2. Pré-requisitos
Certifique-se de que a API REST está habilitada no arquivo `config` do Oxidized:
`rest: 0.0.0.0:8888`

## 3. Configuração no Zabbix (Template LLD)

A estratégia utiliza **LLD (Low-Level Discovery)** com **HTTP Agent**.

### 3.1. Item Mestre (HTTP Agent)
Este item baixa o JSON completo uma única vez.
* **Key:** `oxidized.get_nodes`
* **URL:** `http://{HOST.CONN}:8888/nodes?format=json`
* **Type:** HTTP agent (Text)

### 3.2. Regra de Descoberta (LLD Rule)
Lê o JSON do Item Mestre e descobre cada switch.
* **Master item:** Oxidized: Get Nodes JSON
* **LLD Macros:** `{#NODE_NAME}` → `$.name`, `{#NODE_STATUS}` → `$.last.status`

### 3.3. Protótipos de Itens e Triggers

#### Item: Status do Último Backup
* **Key:** `oxidized.node.status[{#NODE_NAME}]`
* **Preprocessing:** JSONPath `$.[?(@.name=='{#NODE_NAME}')].last.status.first()`

#### Trigger: Falha de Backup
* **Expression:** `last() <> "success"`
* **Severity:** High
* **Nome:** Backup falhou para o host {#NODE_NAME}

#### Trigger: Backup Obsoleto (>24h)
* **Expression:** `fuzzytime(..., 86400) = 0`
* **Severity:** Warning