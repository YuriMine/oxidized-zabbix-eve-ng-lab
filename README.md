# Oxidized + Zabbix + EVE-NG Lab

Laboratório prático para backup, versionamento e monitoramento de
configurações de dispositivos de rede Cisco IOS utilizando:

- Oxidized
- Zabbix
- EVE-NG
- Git

## Objetivo
- Backup automático de configurações
- Versionamento com histórico (Git)
- Integração com monitoramento (Zabbix)
- Ambiente de testes com Cisco 2960 no EVE-NG

## Arquitetura
- Dispositivos Cisco IOS virtualizados no EVE-NG
- Oxidized coletando configs via SSH
- Repositório Git para versionamento
- Zabbix monitorando dispositivos e serviço Oxidized

## Documentação
A documentação completa do laboratório está disponível no diretório `docs/`.
