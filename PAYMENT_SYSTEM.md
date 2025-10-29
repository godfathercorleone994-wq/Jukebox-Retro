# Sistema de Pagamento e Administração - Jukebox Retro

## 📋 Visão Geral

O Jukebox Retro agora inclui um sistema completo de pagamento e administração que permite:

- 💳 **Sistema de Pagamentos**: Suporte para PIX, Dinheiro, Débito e Crédito
- 💰 **Sistema de Créditos**: Usuários podem adicionar créditos para tocar músicas
- 📊 **Estatísticas de Uso**: Rastreamento completo de músicas tocadas e métodos de pagamento
- ⚙️ **Painel Administrativo**: Sistema completo de administração
- 💵 **Caixa**: Sistema de controle de entradas e saídas

## 🔐 Sistema de Autenticação

### Login Padrão
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Créditos iniciais**: R$ 1000,00

### Tipos de Usuário
- **Admin**: Acesso total ao sistema, pode adicionar créditos gratuitamente
- **User**: Usuário regular, precisa pagar para adicionar créditos

## 💰 Sistema de Créditos

### Como Funciona
1. Cada música custa **R$ 1,00** (configurável)
2. Usuários podem tocar músicas usando:
   - Créditos previamente adicionados
   - Pagamento direto por música

### Adicionar Créditos
1. Clique no botão "💰 ADD CRÉDITOS"
2. Digite o valor desejado
3. Selecione o método de pagamento:
   - 📱 **PIX**: Pagamento via PIX
   - 💵 **DINHEIRO**: Pagamento em dinheiro
   - 💳 **DÉBITO**: Cartão de débito
   - 💳 **CRÉDITO**: Cartão de crédito
   - ⭐ **GRÁTIS (ADMIN)**: Apenas para administradores

## 💳 Sistema de Pagamento

### Quando o Pagamento é Solicitado
O sistema solicita pagamento quando:
- Usuário tenta tocar uma música sem créditos suficientes
- Usuário clica em "▶ PLAY"
- Usuário pula para próxima/anterior música
- Usuário clica duas vezes em uma música na playlist

### Métodos de Pagamento Disponíveis
- **PIX**: Pagamento instantâneo
- **DINHEIRO**: Pagamento em espécie
- **DÉBITO**: Cartão de débito
- **CRÉDITO**: Cartão de crédito

### Fluxo de Pagamento
```
1. Usuário tenta tocar música
   ↓
2. Sistema verifica créditos disponíveis
   ↓
3a. Se tem créditos → Debita e toca música
   OU
3b. Se não tem créditos → Mostra diálogo de pagamento
   ↓
4. Usuário seleciona método de pagamento
   ↓
5. Sistema registra transação
   ↓
6. Música é tocada
```

## ⚙️ Painel Administrativo

### Acesso
- Disponível apenas para usuários com role **ADMIN**
- Clique no botão "⚙ ADMIN" no topo da tela

### Abas do Painel

#### 📊 Estatísticas
Mostra informações detalhadas sobre o uso do sistema:
- Total de músicas tocadas
- Receita total gerada
- Distribuição por métodos de pagamento
- Top 10 músicas mais tocadas

**Exemplo de Estatísticas:**
```
╔══════════════════════════════════════════════════════════════╗
║              ESTATÍSTICAS DE USO - JUKEBOX RETRO             ║
╚══════════════════════════════════════════════════════════════╝

📊 RESUMO GERAL
────────────────────────────────────────────────────────────────
  Total de Músicas Tocadas: 150
  Receita Total: R$ 150.00
  Custo por Música: R$ 1.00

💳 MÉTODOS DE PAGAMENTO
────────────────────────────────────────────────────────────────
  PIX: 50 (33.3%)
  DINHEIRO: 30 (20.0%)
  DÉBITO: 40 (26.7%)
  CRÉDITO: 20 (13.3%)
  CRÉDITOS: 10 (6.7%)

🎵 TOP 10 MÚSICAS MAIS TOCADAS
────────────────────────────────────────────────────────────────
  1. Artist A - Song 1 - 15x
  2. Artist B - Song 2 - 12x
  ...
```

#### 💰 Caixa
Sistema de controle de caixa com:
- **Saldo total** do caixa
- **Saldo por método de pagamento**:
  - PIX
  - Dinheiro
  - Débito
  - Crédito
- **Histórico de movimentações** (últimas 100 entradas)

**Formato do Histórico:**
```
DD/MM/YYYY HH:MM | +/-R$ XX.XX | método | descrição
```

#### 👥 Usuários
Gerenciamento de usuários:
- Lista todos os usuários cadastrados
- Mostra role (ADMIN/USER) e créditos
- Permite adicionar novos usuários

**Adicionar Novo Usuário:**
1. Clique em "➕ Adicionar Novo Usuário"
2. Preencha os dados:
   - Username
   - Password
   - Role (User/Admin)
   - Créditos iniciais
3. Clique em "Criar"

#### 💳 Transações
Histórico completo de transações:
- Data e hora
- Usuário
- Valor
- Método de pagamento
- Descrição
- Mostra últimas 200 transações

## 📊 Sistema de Estatísticas

### Dados Rastreados
O sistema registra automaticamente:

1. **Transações**: Todas as movimentações financeiras
   - ID da transação
   - Usuário
   - Método de pagamento
   - Valor
   - Descrição
   - Timestamp

2. **Registros de Uso**: Cada música tocada
   - ID do registro
   - Usuário
   - Título da música
   - Artista
   - Método de pagamento usado
   - Custo
   - Timestamp

3. **Caixa**: Entradas e saídas
   - ID da entrada
   - Tipo (income/expense)
   - Valor
   - Método de pagamento
   - Descrição
   - Timestamp

### Análises Disponíveis
- Total de músicas tocadas
- Receita total gerada
- Músicas mais populares
- Métodos de pagamento mais usados
- Saldo do caixa por método

## 💾 Armazenamento de Dados

### Localização
Todos os dados são salvos em: `~/.jukebox_retro/`

### Arquivos de Dados
- `users.json`: Usuários cadastrados
- `transactions.json`: Histórico de transações
- `usage_stats.json`: Estatísticas de uso
- `cash_register.json`: Movimentações do caixa
- `config.json`: Configurações gerais (playlist, volume)

### Estrutura dos Dados

#### Users (users.json)
```json
[
  {
    "username": "admin",
    "password_hash": "hash_here",
    "role": "admin",
    "credits": 1000.0,
    "created_at": "2025-01-01T10:00:00"
  }
]
```

#### Transactions (transactions.json)
```json
[
  {
    "transaction_id": "uuid",
    "username": "admin",
    "payment_method": "pix",
    "amount": 10.0,
    "description": "Recarga de créditos",
    "timestamp": "2025-01-01T10:30:00"
  }
]
```

#### Usage Stats (usage_stats.json)
```json
[
  {
    "record_id": "uuid",
    "username": "admin",
    "song_title": "Song Title",
    "song_artist": "Artist Name",
    "played_at": "2025-01-01T11:00:00",
    "payment_method": "créditos",
    "cost": 1.0
  }
]
```

#### Cash Register (cash_register.json)
```json
[
  {
    "entry_id": "uuid",
    "entry_type": "income",
    "amount": 10.0,
    "payment_method": "pix",
    "description": "Recarga de créditos",
    "timestamp": "2025-01-01T10:30:00"
  }
]
```

## 🔒 Segurança

### Autenticação
- Senhas são armazenadas como hash SHA-256
- Sistema de login obrigatório
- Separação de privilégios (Admin vs User)

### ⚠️ AVISO DE SEGURANÇA - IMPORTANTE
**A implementação atual usa SHA-256 para hash de senhas, que é adequado apenas para demonstração e protótipos.**

Para uso em produção, é **CRÍTICO** substituir o método de hashing por uma das seguintes alternativas seguras:

1. **bcrypt** (Recomendado):
```python
import bcrypt

def _hash_password(self, password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(self, password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
```

2. **argon2** (Recomendado):
```python
from argon2 import PasswordHasher

ph = PasswordHasher()

def _hash_password(self, password: str) -> str:
    return ph.hash(password)

def verify_password(self, password: str, password_hash: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except:
        return False
```

**Por que SHA-256 não é seguro para senhas:**
- É muito rápido, permitindo ataques de força bruta
- Não usa salt automaticamente
- Vulnerável a rainbow tables
- Não é projetado para hashing de senhas

### Controle de Acesso
- **Painel Admin**: Apenas para usuários admin
- **Créditos Grátis**: Apenas administradores podem adicionar
- **Usuários normais**: Devem pagar para adicionar créditos

### Recomendações de Produção
⚠️ **IMPORTANTE**: Para uso em produção, recomenda-se:
1. **Usar bcrypt ou argon2 para hash de senhas** (CRÍTICO)
2. Implementar timeout de sessão
3. Adicionar logs de auditoria
4. Usar banco de dados ao invés de JSON
5. Adicionar backup automático dos dados
6. Implementar rate limiting para tentativas de login
7. Adicionar autenticação de dois fatores (2FA)
8. Usar HTTPS se houver acesso remoto
9. Validar e sanitizar todas as entradas de usuário
10. Implementar políticas de senha forte

## 🎯 Casos de Uso

### Caso 1: Usuário Regular Tocando Música
1. Login com credenciais de usuário regular
2. Adiciona música à playlist
3. Clica em PLAY
4. Como não tem créditos, sistema mostra diálogo de pagamento
5. Seleciona PIX como método
6. Música é tocada
7. Transação é registrada no sistema

### Caso 2: Admin Adicionando Créditos Gratuitamente
1. Login como admin
2. Clica em "💰 ADD CRÉDITOS"
3. Digite valor (ex: 100.00)
4. Seleciona "⭐ GRÁTIS (ADMIN)"
5. Créditos são adicionados sem custo
6. Transação é registrada (mas não entra no caixa)

### Caso 3: Admin Visualizando Estatísticas
1. Login como admin
2. Clica em "⚙ ADMIN"
3. Navega pelas abas:
   - Vê estatísticas de uso
   - Verifica saldo do caixa
   - Analisa transações
   - Gerencia usuários

## 📱 Interface do Usuário

### Elementos Novos na Tela Principal
- **Barra Superior**:
  - Informações do usuário (nome, role, créditos)
  - Botão "💰 ADD CRÉDITOS"
  - Botão "⚙ ADMIN" (apenas para admins)

### Diálogos
1. **Login**: Tela inicial de autenticação
2. **Pagamento**: Seleção de método de pagamento
3. **Adicionar Créditos**: Interface para recarga
4. **Admin Panel**: Painel completo com 4 abas
5. **Novo Usuário**: Formulário para criar usuários

## 🚀 Começando

### Primeiro Acesso
1. Execute o aplicativo
2. Faça login com:
   - Username: `admin`
   - Password: `admin123`
3. Adicione músicas à playlist
4. Clique em PLAY (admin tem 1000 créditos por padrão)
5. Explore o painel administrativo

### Criando um Usuário Regular
1. Acesse o painel admin
2. Vá para a aba "👥 Usuários"
3. Clique em "➕ Adicionar Novo Usuário"
4. Preencha:
   - Username: `user1`
   - Password: `senha123`
   - Role: `User`
   - Créditos iniciais: `0.0`
5. Clique em "Criar"

### Testando o Sistema de Pagamento
1. Saia do admin e faça login com `user1`
2. Tente tocar uma música
3. Sistema solicitará pagamento
4. Selecione um método de pagamento
5. Música é tocada

## 🔧 Configurações

### Alterar Custo por Música
Edite no código `jukebox_retro.py`:
```python
self.song_cost = 1.0  # Altere este valor
```

### Personalizar Métodos de Pagamento
Adicione novos métodos em `models.py`:
```python
class PaymentMethod(Enum):
    PIX = "pix"
    CASH = "dinheiro"
    DEBIT = "débito"
    CREDIT = "crédito"
    CREDITS = "créditos"
    # Adicione novos aqui
    NOVO_METODO = "novo_metodo"
```

## 📈 Melhorias Futuras Sugeridas

1. **Relatórios em PDF**: Exportar estatísticas e relatórios
2. **Gráficos**: Visualização gráfica das estatísticas
3. **Backup automático**: Sistema de backup dos dados
4. **API REST**: Interface para integração com outros sistemas
5. **QR Code PIX**: Geração de QR Code para pagamentos PIX
6. **Histórico de créditos**: Ver histórico de adição de créditos
7. **Permissões granulares**: Mais níveis de acesso
8. **Notificações**: Alertas para administradores
9. **Temas customizáveis**: Personalização da interface
10. **Multi-idioma**: Suporte para outros idiomas

## 🐛 Solução de Problemas

### Esqueci a senha do admin
1. Delete o arquivo `~/.jukebox_retro/users.json`
2. Reinicie o aplicativo
3. Usuário admin padrão será recriado

### Dados corrompidos
1. Faça backup da pasta `~/.jukebox_retro/`
2. Delete os arquivos JSON problemáticos
3. Reinicie o aplicativo
4. Arquivos serão recriados

### Créditos não estão atualizando
1. Verifique se o arquivo `users.json` tem permissão de escrita
2. Reinicie o aplicativo
3. Verifique logs de erro no console

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs no console
2. Consulte esta documentação
3. Abra uma issue no repositório GitHub
4. Entre em contato com o desenvolvedor

---

**Desenvolvido com ❤️ para o Jukebox Retro**
