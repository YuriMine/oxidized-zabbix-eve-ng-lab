---

### `docs/integracao-zabbix.md`

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