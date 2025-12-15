# Projeto de Automação de Backup de Rede: Oxidized + Zabbix + EVE-NG

## Resumo Executivo
Este repositório contém a documentação técnica e scripts para a implementação de um sistema automatizado de backup e versionamento de configurações de ativos de rede. A solução utiliza o **Oxidized** como motor de coleta, **Git** para versionamento histórico e **Zabbix** como fonte de inventário (Source of Truth) e monitoramento de saúde.

O ambiente de validação foi construído utilizando **EVE-NG** simulando switches Cisco IOS (2960).

## Estrutura da Documentação

A documentação está dividida nos seguintes módulos dentro do diretório `docs/`:

1. **[Arquitetura](Docs/arquitetura.md)**: Visão geral dos componentes, fluxo de dados e design da solução.
2. **[Instalação](Docs/instalacao.md)**: Requisitos de SO, dependências, instalação das Gems Ruby e configuração do serviço Systemd.
3. **[Configuração Oxidized](Docs/configuracao.md)**: Detalhamento do arquivo `config`, parâmetros de coleta e preparação dos ativos Cisco IOS.
4. **[Integração Zabbix](Docs/integracao-zabbix.md)**: Metodologia para tornar o inventário dinâmico via API do Zabbix.
5. **[Monitoramento de Saúde](Docs/monitoramento-zabbix.md)**: Configuração de alertas no Zabbix para falhas de backup.
6. **[Troubleshooting](Docs/troubleshooting.md)**: Guia de resolução de problemas comuns (SSH, Permissões, PID).

## Scripts
O diretório `scripts/` contém exemplos de integração para consumo da API do Zabbix.