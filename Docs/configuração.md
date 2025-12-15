# Configuracao do Oxidized e Ativos de Rede

## 1. Estrutura de Diretorios
A configuracao reside padronizadamente em `/home/oxidized/.config/oxidized/`.
Execute o comando `oxidized` uma vez manualmente para gerar a estrutura inicial se ela nao existir.

## 2. Arquivo Principal (config)
Caminho: `/home/oxidized/.config/oxidized/config`
Abaixo, a configuracao otimizada para ambiente Cisco IOS.

```yaml
---
username: admin           # Credencial padrao SSH
password: admin123        # Senha padrao
enable: admin123          # Senha de Enable
model: ios                # Driver padrao
interval: 3600            # Intervalo em segundos (1 hora)
use_syslog: false
debug: false
threads: 30               # Conexoes simultaneas
timeout: 20               # Timeout SSH
retries: 3

prompt: !ruby/regexp /^([\w.@()-]+[#>])$/

rest: 0.0.0.0:8888        # Interface Web

# Mapeamento de variaveis globais
vars:
  enable: admin123
  remove_secret: true     # Tenta mascarar senhas na config

# Fonte de Inventario (Inicialmente arquivo estatico)
source:
  default: csv
  csv:
    file: /home/oxidized/.config/oxidized/router.db
    delimiter: ':'
    map:
      name: 0
      ip: 1
      model: 2

# Saida (Git Local)
output:
  default: git
  git:
    user: Oxidized Automation
    email: oxidized@lab.local
    repo: /home/oxidized/.config/oxidized/network_configs.git