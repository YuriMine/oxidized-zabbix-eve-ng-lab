# Script de Integração: Zabbix Importer

Este script é responsável por conectar na API do Zabbix, buscar hosts de um grupo específico e atualizar o arquivo `router.db` do Oxidized.

### `scripts/zabbix_importer.py`

```python
#!/usr/bin/env python3
import requests
import json
import csv
import sys

# --- Configurações ---
# Ajuste estas variáveis conforme seu ambiente
ZABBIX_URL = "[http://192.168.1.100/zabbix/api_jsonrpc.php](http://192.168.1.100/zabbix/api_jsonrpc.php)"
ZABBIX_USER = "Admin"
ZABBIX_PASS = "zabbix"
ROUTER_DB_PATH = "/home/oxidized/.config/oxidized/router.db"
GROUP_ID = "2" # ID do grupo de Switches no Zabbix

def get_auth_token():
    """Autentica no Zabbix e retorna o Token de Sessão"""
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {"user": ZABBIX_USER, "password": ZABBIX_PASS},
        "id": 1
    }
    try:
        resp = requests.post(ZABBIX_URL, json=payload)
        return resp.json().get('result')
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

def get_hosts(token, group_id):
    """Busca hosts habilitados de um grupo específico"""
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["host", "name"],
            "selectInterfaces": ["ip"],
            "groupids": group_id,
            "filter": {"status": "0"} # 0 = Monitorado/Habilitado
        },
        "auth": token,
        "id": 2
    }
    resp = requests.post(ZABBIX_URL, json=payload)
    return resp.json().get('result', [])

def main():
    print("--- Iniciando Sincronização Zabbix -> Oxidized ---")
    
    token = get_auth_token()
    if not token:
        print("Erro: Falha na autenticação com o Zabbix.")
        sys.exit(1)

    hosts = get_hosts(token, GROUP_ID)
    
    if not hosts:
        print("Aviso: Nenhum host encontrado no grupo especificado.")
        sys.exit(0)

    print(f"📡 Hosts encontrados: {len(hosts)}")

    try:
        with open(ROUTER_DB_PATH, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=':')
            count = 0
            for host in hosts:
                # Tenta pegar o IP da primeira interface
                try:
                    ip = host['interfaces'][0]['ip']
                    name = host['name']
                    # Define driver padrão como 'ios' (Pode ser melhorado para dinâmico)
                    writer.writerow([name, ip, 'ios'])
                    count += 1
                except (IndexError, KeyError):
                    print(f"⚠️ Pulo: Host {host['name']} sem interface IP válida.")
                    continue
        
        print(f"Sucesso: {count} dispositivos exportados para {ROUTER_DB_PATH}")
        
    except PermissionError:
        print(f"Erro: Sem permissão de escrita em {ROUTER_DB_PATH}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```