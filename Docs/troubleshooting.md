# Troubleshooting e Resoluções Comuns

## 1. Erros de SSH (Key Exchange / Algorithms)
Equipamentos Cisco antigos podem usar algoritmos de criptografia que o OpenSSH moderno desabilita por padrão (segurança).

**Sintoma:** O log mostra `Net::SSH::Exception: handshake failed`.

**Solução:** Editar o arquivo `~/.ssh/config` do usuário oxidized:
```text
Host 192.168.*.*
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    Ciphers +aes128-cbc,3des-cbc,aes256-cbc

    Com certeza. Abaixo estão todos os arquivos separadamente, incluindo o novo módulo de monitoramento, prontos para você copiar e colar na sua estrutura de projeto.

📄 README.md
Markdown

# Projeto de Automação de Backup de Rede: Oxidized + Zabbix + EVE-NG

## Resumo Executivo
Este repositório contém a documentação técnica e scripts para a implementação de um sistema automatizado de backup e versionamento de configurações de ativos de rede. A solução utiliza o **Oxidized** como motor de coleta, **Git** para versionamento histórico e **Zabbix** como fonte de inventário (Source of Truth) e monitoramento de saúde.

O ambiente de validação foi construído utilizando **EVE-NG** simulando switches Cisco IOS (2960).

## Estrutura da Documentação

A documentação está dividida nos seguintes módulos dentro do diretório `docs/`:

1. **[Arquitetura](docs/arquitetura.md)**: Visão geral dos componentes, fluxo de dados e design da solução.
2. **[Instalação](docs/instalacao.md)**: Requisitos de SO, dependências, instalação das Gems Ruby e configuração do serviço Systemd.
3. **[Configuração Oxidized](docs/configuracao-oxidized.md)**: Detalhamento do arquivo `config`, parâmetros de coleta e preparação dos ativos Cisco IOS.
4. **[Integração Zabbix](docs/integracao-zabbix.md)**: Metodologia para tornar o inventário dinâmico via API do Zabbix.
5. **[Monitoramento de Saúde](docs/monitoramento-zabbix.md)**: Configuração de alertas no Zabbix para falhas de backup.
6. **[Troubleshooting](docs/troubleshooting.md)**: Guia de resolução de problemas comuns (SSH, Permissões, PID).

## Scripts
O diretório `scripts/` contém exemplos de integração para consumo da API do Zabbix.
📄 docs/arquitetura.md
Markdown

# Arquitetura da Solução

## 1. Visão Geral
O objetivo desta arquitetura é eliminar o backup manual de configurações e prover auditoria de mudanças na rede. O sistema opera de forma não intrusiva, acessando os equipamentos via SSH, coletando as configurações e armazenando-as em um repositório Git local.

## 2. Componentes do Sistema

### 2.1 EVE-NG (Camada de Simulação)
Ambiente de laboratório responsável por hospedar as imagens virtuais dos switches Cisco 2960. Permite a validação de comandos SSH e testes de conectividade antes da implementação em produção.

### 2.2 Oxidized (Motor de Coleta)
Software desenvolvido em Ruby que gerencia a fila de dispositivos, realiza a conexão SSH, trata a saída (removendo segredos ou linhas irrelevantes como tempo de uptime) e entrega o resultado para o sistema de versionamento.

### 2.3 Git (Camada de Armazenamento)
Diferente de sistemas que apenas salvam arquivos de texto com data e hora, o Git armazena apenas o diferencial (delta) entre as coletas. Isso permite:
* Identificar exatamente o que mudou (Diff).
* Identificar quando mudou.
* Rastreabilidade de autoria (quando integrado a sistemas de CI/CD).
* Economia de espaço em disco.

### 2.4 Zabbix (Camada de Gerência)
Atua como a "Single Source of Truth" (Fonte Única da Verdade) para o inventário e Monitoramento.
* **Inventário:** O Oxidized consulta o Zabbix para saber quais dispositivos devem ter backup realizado.
* **Monitoramento:** O Zabbix consulta o Oxidized para saber se os backups estão ocorrendo com sucesso.

## 3. Fluxo de Dados

1. **Discovery:** Script ou Módulo HTTP do Oxidized consulta a API do Zabbix para obter a lista de IPs ativos.
2. **Coleta:** Oxidized conecta via SSH nos Switches (simulados no EVE-NG ou físicos).
3. **Processamento:** Oxidized normaliza a saída da configuração.
4. **Armazenamento:** Oxidized realiza um `git commit` e `git push` no repositório local.
5. **Auditoria:** Zabbix consome a API REST do Oxidized para verificar status `success` ou `fail`.
📄 docs/instalacao.md
Markdown

# Guia de Instalação e Preparação do Servidor

## 1. Requisitos do Sistema
* **Sistema Operacional:** Ubuntu Server 22.04 LTS (Recomendado).
* **Hardware Mínimo:** 2 vCPU, 4GB RAM, 20GB Disco.
* **Rede:** Acesso SSH aos ativos de rede e acesso HTTP/HTTPS à API do Zabbix.

## 2. Preparação do Ambiente
É altamente recomendado criar um usuário dedicado para o serviço, evitando a execução como `root`.

```bash
# Criação do usuário
sudo useradd -m -s /bin/bash oxidized

# Atualização e Dependências do Sistema
sudo apt update
sudo apt install -y git ruby ruby-dev libsqlite3-dev libssl-dev libssh2-1-dev cmake make curl pkg-config libicu-dev zlib1g-dev g++
3. Instalação do Oxidized
A instalação é feita via gerenciador de pacotes Ruby (Gems).

Bash

# Instalar componentes principais
sudo gem install oxidized oxidized-web oxidized-script
4. Configuração do Serviço (Systemd)
Para garantir que o Oxidized inicie automaticamente e reinicie em caso de falhas. Crie o arquivo /etc/systemd/system/oxidized.service:

Ini, TOML

[Unit]
Description=Oxidized Network Configuration Backup
After=network.target

[Service]
User=oxidized
Group=oxidized
WorkingDirectory=/home/oxidized
ExecStart=/usr/local/bin/oxidized
Restart=on-failure
RestartSec=30s
Environment="OXIDIZED_HOME=/home/oxidized/.config/oxidized"

[Install]
WantedBy=multi-user.target
Ativação do serviço:

Bash

sudo systemctl daemon-reload
sudo systemctl enable oxidized
sudo systemctl start oxidized

---

### 📄 `docs/configuracao-oxidized.md`

```markdown
# Configuração do Oxidized e Ativos de Rede

## 1. Estrutura de Diretórios
A configuração reside padronizadamente em `/home/oxidized/.config/oxidized/`.
Execute o comando `oxidized` uma vez manualmente para gerar a estrutura inicial se ela não existir.

## 2. Arquivo Principal (config)
Caminho: `/home/oxidized/.config/oxidized/config`
Abaixo, a configuração otimizada para ambiente Cisco IOS com API REST habilitada.

```yaml
---
username: admin           # Credencial padrão SSH
password: admin123        # Senha padrão
enable: admin123          # Senha de Enable
model: ios                # Driver padrão
interval: 3600            # Intervalo em segundos (1 hora)
use_syslog: false
debug: false
threads: 30               # Conexões simultâneas
timeout: 20               # Timeout SSH
retries: 3

prompt: !ruby/regexp /^([\w.@()-]+[#>])$/

# API REST para integração com Zabbix
rest: 0.0.0.0:8888

# Mapeamento de variáveis globais
vars:
  enable: admin123
  remove_secret: true     # Tenta mascarar senhas na config

# Fonte de Inventário (Inicialmente arquivo estático)
source:
  default: csv
  csv:
    file: /home/oxidized/.config/oxidized/router.db
    delimiter: ':'
    map:
      name: 0
      ip: 1
      model: 2

# Saída (Git Local)
output:
  default: git
  git:
    user: Oxidized Automation
    email: oxidized@lab.local
    repo: /home/oxidized/.config/oxidized/network_configs.git
3. Arquivo de Inventário (router.db)
Utilizado quando a integração automática com Zabbix não está ativa. Formato: HOSTNAME:IP:DRIVER

Plaintext

SW-CORE-01:192.168.10.1:ios
SW-ACC-01:192.168.10.2:ios
SW-ACC-02:192.168.10.3:ios
4. Preparação dos Switches (Cisco IOS)
Para o correto funcionamento, o switch deve aceitar conexões SSH não-interativas.

Snippet de código

! Configuração Global
hostname SW-LAB-01
ip domain-name lab.local
crypto key generate rsa modulus 2048
ip ssh version 2

! Usuário com privilégio máximo
username admin privilege 15 secret admin123

! Configuração de linhas VTY
line vty 0 4
 transport input ssh
 login local
!

---

### 📄 `docs/integracao-zabbix.md`

```markdown
# Integração Dinâmica: Zabbix como Fonte de Verdade

## 1. Conceito
Manter um arquivo `router.db` manual é ineficiente e propenso a erro humano em grandes redes. A integração visa automatizar a população de dispositivos no Oxidized baseando-se no monitoramento do Zabbix.

## 2. Estratégia de Implementação
Existem dois métodos principais:

1.  **Script Middleware (Recomendado):** Um script Python consulta a API do Zabbix, filtra hosts por um Grupo ou Tag específica (ex: "Network Devices") e gera o arquivo CSV `router.db`.
2.  **Oxidized HTTP Source:** O Oxidized faz uma requisição direta a uma URL que retorna JSON.

## 3. Requisitos no Zabbix
1.  **Grupo de Hosts:** Criar um grupo chamado "Oxidized Backup" ou utilizar um existente.
2.  **Usuário de API:** Criar um usuário no Zabbix com permissões de leitura (Read-only) neste grupo.

## 4. Fluxo de Automação (Cronjob)
Podemos configurar um Cronjob no servidor Linux para atualizar a lista de dispositivos a cada hora.

Exemplo de entrada no Crontab (`crontab -e -u oxidized`):
```bash
# Atualiza a lista de dispositivos do Zabbix a cada hora e recarrega o Oxidized
0 * * * * python3 /home/oxidized/scripts/zabbix_importer.py && pkill -HUP oxidized
Consulte o diretório scripts/ para visualizar o código fonte do importador.


---

### 📄 `docs/monitoramento-zabbix.md`

```markdown
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

docs/troubleshooting.md
Markdown

# Troubleshooting e Resoluções Comuns

## 1. Erros de SSH (Key Exchange / Algorithms)
Equipamentos Cisco antigos podem usar algoritmos de criptografia que o OpenSSH moderno desabilita por padrão (segurança).

**Sintoma:** O log mostra `Net::SSH::Exception: handshake failed`.

**Solução:** Editar o arquivo `~/.ssh/config` do usuário oxidized:
```text
Host 192.168.*.*
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    Ciphers +aes128-cbc,3des-cbc,aes256-cbc
2. Processo Travado (PID File)
Se o servidor desligar abruptamente ou faltar energia, o arquivo de PID pode impedir o reinício.

Sintoma: A server is already running. Check /pid/oxidized.pid.

Solução:

Bash

rm /home/oxidized/.config/oxidized/pid/oxidized.pid
systemctl start oxidized
3. Permissões de Arquivo
Sintoma: Errno::EACCES: Permission denied.

Solução: Garantir recursividade de dono para o usuário do serviço.

Bash

sudo chown -R oxidized:oxidized /home/oxidized/.config/
4. Debugging
Para visualizar exatamente o que está acontecendo durante a conexão (troubleshooting avançado):

Pare o serviço: systemctl stop oxidized

Execute manualmente com debug: oxidized --debug

Analise a saída no terminal para identificar onde a coleta trava (login, prompt, comando específico).


---

### 📄 `scripts/zabbix_importer.py`

```python
#!/usr/bin/env python3
import requests
import json
import csv

# --- Configurações ---
ZABBIX_URL = "http://192.168.1.100/zabbix/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASS = "zabbix"
ROUTER_DB_PATH = "/home/oxidized/.config/oxidized/router.db"
GROUP_ID = "2" # ID do grupo de Switches no Zabbix

def get_auth_token():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {"user": ZABBIX_USER, "password": ZABBIX_PASS},
        "id": 1
    }
    resp = requests.post(ZABBIX_URL, json=payload)
    return resp.json().get('result')

def get_hosts(token, group_id):
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["host", "name"],
            "selectInterfaces": ["ip"],
            "groupids": group_id,
            "filter": {"status": "0"} # Apenas hosts habilitados
        },
        "auth": token,
        "id": 2
    }
    resp = requests.post(ZABBIX_URL, json=payload)
    return resp.json().get('result')

def main():
    token = get_auth_token()
    if not token:
        print("Erro de autenticação no Zabbix")
        exit(1)

    hosts = get_hosts(token, GROUP_ID)
    
    with open(ROUTER_DB_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=':')
        for host in hosts:
            # Assume a primeira interface como IP de gerencia
            try:
                ip = host['interfaces'][0]['ip']
                name = host['name']
                # Define driver padrão como 'ios'
                writer.writerow([name, ip, 'ios'])
            except IndexError:
                continue
                
    print(f"Exportados {len(hosts)} hosts para {ROUTER_DB_PATH}")

if __name__ == "__main__":
    main()