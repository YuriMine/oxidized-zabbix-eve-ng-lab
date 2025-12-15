# Troubleshooting e Resoluções Comuns

## 1. Erros de SSH (Key Exchange / Algorithms)
Equipamentos Cisco antigos podem usar algoritmos de criptografia que o OpenSSH moderno desabilita por padrão (segurança).

**Sintoma:** O log mostra `Net::SSH::Exception: handshake failed`.

**Solução:** Editar o arquivo `~/.ssh/config` do usuário oxidized:

Host 192.168.*.*
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    Ciphers +aes128-cbc,3des-cbc,aes256-cbc
## 2. Processo Travado (PID File)
Se o servidor desligar abruptamente ou faltar energia, o arquivo de PID pode impedir o reinício.

Sintoma: A server is already running. Check /pid/oxidized.pid.

Solução:

bash
rm /home/oxidized/.config/oxidized/pid/oxidized.pid
systemctl start oxidized

## 3. Permissões de Arquivo
Sintoma: Errno::EACCES: Permission denied.

Solução: Garantir recursividade de dono para o usuário do serviço.

bash
sudo chown -R oxidized:oxidized /home/oxidized/.config/
## 4. Debugging
Para visualizar exatamente o que está acontecendo durante a conexão (troubleshooting avançado):

Pare o serviço: systemctl stop oxidized

Execute manualmente com debug: 

bash
oxidized --debug

Analise a saída no terminal para identificar onde a coleta trava (login, prompt, comando específico).