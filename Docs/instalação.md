# Guia de Instalacao e Preparacao do Servidor

## 1. Requisitos do Sistema
* **Sistema Operacional:** Ubuntu Server 22.04 LTS (Recomendado).
* **Hardware Minimo:** 2 vCPU, 4GB RAM, 20GB Disco.
* **Rede:** Acesso SSH aos ativos de rede e acesso HTTP/HTTPS a API do Zabbix.

## 2. Preparacao do Ambiente
E altamente recomendado criar um usuario dedicado para o servico, evitando a execucao como `root`.

```bash
# Criacao do usuario
sudo useradd -m -s /bin/bash oxidized

# Atualizacao e Dependencias do Sistema
sudo apt update
sudo apt install -y git ruby ruby-dev libsqlite3-dev libssl-dev libssh2-1-dev cmake make curl pkg-config libicu-dev zlib1g-dev g++