# Projeto de Automacao de Backup de Rede: Oxidized + Zabbix + EVE-NG

## Resumo Executivo
Este repositorio contem a documentacao tecnica e scripts para a implementacao de um sistema automatizado de backup e versionamento de configuracoes de ativos de rede. A solucao utiliza o **Oxidized** como motor de coleta, **Git** para versionamento historico e **Zabbix** como fonte de inventario (Source of Truth).

O ambiente de validacao foi construido utilizando **EVE-NG** simulando switches Cisco IOS (2960).

## Estrutura da Documentacao

A documentacao esta dividida nos seguintes modulos dentro do diretorio `docs/`:

1. **[Arquitetura](docs/arquitetura.md)**: Visao geral dos componentes, fluxo de dados e design da solucao.
2. **[Instalacao](docs/instalacao.md)**: Requisitos de SO, dependencias, instalacao das Gems Ruby e configuracao do servico Systemd.
3. **[Configuracao Oxidized](docs/configuracao-oxidized.md)**: Detalhamento do arquivo `config`, parametros de coleta e preparacao dos ativos Cisco IOS.
4. **[Integracao Zabbix](docs/integracao-zabbix.md)**: Metodologia para tornar o inventario dinamico via API do Zabbix.
5. **[Troubleshooting](docs/troubleshooting.md)**: Guia de resolucao de problemas comuns (SSH, Permissoes, PID).

## Scripts
O diretorio `scripts/` contem exemplos de integracao para consumo da API do Zabbix.