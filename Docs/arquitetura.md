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