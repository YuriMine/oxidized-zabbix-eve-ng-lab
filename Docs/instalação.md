# Guia de Instalacao e Preparacao do Servidor

## 1. Requisitos do Sistema
* **Sistema Operacional:** Ubuntu Server 22.04 LTS (Recomendado).
* **Hardware Minimo:** 2 vCPU, 4GB RAM, 20GB Disco.
* **Rede:** Acesso SSH aos ativos de rede e acesso HTTP/HTTPS a API do Zabbix.

## 2. Preparacao do Ambiente
E altamente recomendado criar um usuario dedicado para o servico, evitando a execucao como `root`.

# Criacao do usuario
sudo useradd -m -s /bin/bash oxidized

## 3. Atualizacao e Dependencias do Sistema
sudo apt update
sudo apt install -y git ruby ruby-dev libsqlite3-dev libssl-dev libssh2-1-dev cmake make curl pkg-config libicu-dev zlib1g-dev g++

## 4. Instalacao do Oxidized
A instalacao e feita via gerenciador de pacotes Ruby (Gems).

## 5. Instalar componentes principais
sudo gem install oxidized oxidized-web oxidized-script

#Configuracao do Servico (Systemd)
Para garantir que o Oxidized inicie automaticamente e reinicie em caso de falhas. Crie o arquivo /etc/systemd/system/oxidized.service:

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
Ativacao do servico:

sudo systemctl daemon-reload
sudo systemctl enable oxidized
sudo systemctl start oxidized
