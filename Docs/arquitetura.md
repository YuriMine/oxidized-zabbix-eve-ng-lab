# Arquitetura do Laboratório


## Visão Geral
O laboratório simula um ambiente real de rede com dispositivos Cisco virtualizados, coleta automática de configurações e versionamento.


## Componentes
- **EVE-NG**: Simulação dos dispositivos Cisco IOS
- **Oxidized**: Backup automático via SSH
- **Git**: Versionamento das configurações
- **Zabbix**: Monitoramento dos dispositivos e serviços
- **GitLab**: Repositório principal
- **GitHub**: Espelho para portfólio


## Fluxo de Dados
1. Dispositivos Cisco são criados no EVE-NG
2. Oxidized acessa via SSH
3. Configurações são coletadas periodicamente
4. Commits automáticos são gerados
5. GitLab espelha para GitHub
6. Zabbix monitora disponibilidade e serviços