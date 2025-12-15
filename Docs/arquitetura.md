# Arquitetura da Solucao

## Visao Geral
O objetivo desta arquitetura e eliminar o backup manual de configuracoes e prover auditoria de mudancas na rede. O sistema opera de forma nao intrusiva, acessando os equipamentos via SSH, coletando as configuracoes e armazenando-as em um repositorio Git local.

## Componentes do Sistema

### 1. EVE-NG (Camada de Simulacao)
Ambiente de laboratorio responsavel por hospedar as imagens virtuais dos switches Cisco 2960. Permite a validacao de comandos SSH e testes de conectividade antes da implementacao em producao.

### 2. Oxidized (Motor de Coleta)
Software desenvolvido em Ruby que gerencia a fila de dispositivos, realiza a conexao SSH, trata a saida (removendo segredos ou linhas irrelevantes) e entrega o resultado para o sistema de versionamento.

### 3. Git (Camada de Armazenamento)
Diferente de sistemas que apenas salvam arquivos `.txt` com data e hora, o Git armazena apenas o diferencial (delta) entre as coletas. Isso permite:
* Identificar exatamente o que mudou (Diff).
* Identificar quando mudou.
* Economia de espaco em disco.

### 4. Zabbix (Camada de Gerencia)
Atua como a fonte da verdade para o inventario. O Oxidized consulta o Zabbix para saber quais dispositivos devem ter backup realizado, garantindo que o monitoramento e o backup estejam sempre sincronizados.

## Fluxo de Dados

1. **Discovery:** Script/Oxidized consulta a API do Zabbix para obter lista de IPs.
2. **Coleta:** Oxidized conecta via SSH nos Switches (EVE-NG).
3. **Processamento:** Oxidized normaliza a saida (remove uptime, temperatura, etc).
4. **Armazenamento:** Oxidized realiza um `git commit` e `git push` no repositorio local.