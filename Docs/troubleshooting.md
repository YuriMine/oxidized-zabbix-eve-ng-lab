# Troubleshooting e Resoluções Comuns

## 1. Erros de SSH (Key Exchange / Algorithms)
Equipamentos Cisco antigos podem usar algoritmos de criptografia que o OpenSSH moderno desabilita por padrão (segurança).

**Sintoma:** O log mostra `Net::SSH::Exception: handshake failed`.

**Solução:** Editar o arquivo `~/.ssh/config` do usuário oxidized:
```text
Host 192.168.*.*
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    Ciphers +aes128-cbc,3des-cbc,aes256-cbc