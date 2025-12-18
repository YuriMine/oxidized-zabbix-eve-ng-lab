# Troubleshooting e Resoluções Comuns

## 1. Erros de SSH (Key Exchange / Algorithms)
Equipamentos Cisco antigos podem usar algoritmos de criptografia que o OpenSSH moderno desabilita por padrão por questões de segurança.
**Sintoma:** O log mostra `Net::SSH::Exception: handshake failed`.

**Solução A (Arquivo de Configuração do Oxidized):**
No arquivo `~/.config/oxidized/config`, adicione as seguintes variáveis na seção `vars` para compatibilidade global:
```yaml
vars:
  ssh_kex: diffie-hellman-group1-sha1
  ssh_host_key: ssh-rsa
  ssh_cipher: aes128-cbc
```

**Solução B (Arquivo SSH do Usuário):**
Editar o arquivo `~/.ssh/config` do usuário oxidized:
```text
Host 192.168.*.*
    KexAlgorithms +diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    Ciphers +aes128-cbc,3des-cbc,aes256-cbc
```

## 2. Processo Travado (PID File)
Se o servidor desligar abruptamente ou faltar energia, o arquivo de PID pode impedir o reinício.
**Sintoma:** `A server is already running. Check /pid/oxidized.pid`.

**Solução:**
Remover o arquivo residual e iniciar o serviço:
```bash
rm /home/oxidized/.config/oxidized/pid/oxidized.pid
systemctl start oxidized
```

## 3. Permissões de Arquivo
**Sintoma:** `Errno::EACCES: Permission denied`.
**Solução:** Garantir recursividade de dono para o usuário do serviço.
```bash
sudo chown -R oxidized:oxidized /home/oxidized/.config/
```

## 4. Escalação de Privilégio (Enable)
O Oxidized trava ao aguardar o prompt de senha do modo `enable`, resultando em timeout na coleta.
**Sintoma:** Log de debug interrompido em `DEBUG -- : lib/oxidized/input/ssh.rb enable @ SW...`.
**Solução:** Configurar o usuário no switch para entrar diretamente no nível 15.
```bash
# No switch Cisco:
conf t
username admin privilege 15 secret senac2010
line vty 0 15
 privilege level 15
exit
wr
```

## 5. Sincronização com GitHub
Backup local atualizado, mas as mudanças não são refletidas no repositório remoto.
**Sintoma:** O `git log` local mostra commits atuais, mas o GitHub permanece desatualizado.
**Solução:** Validar o Token (PAT) e forçar o sincronismo manual para alinhar os históricos:
```bash
cd /home/oxidized/.config/oxidized/network_configs.git
git push origin master -f
```

## 6. Debugging
Para visualizar exatamente o que está acontecendo durante a conexão (troubleshooting avançado):
Pare o serviço:
```bash
systemctl stop oxidized
```
Execute manualmente com debug para identificar onde a coleta trava (login, prompt, comando específico):
```bash
su - oxidized
oxidized --debug
```