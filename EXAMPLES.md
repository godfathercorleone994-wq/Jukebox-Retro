# Exemplos de Uso - Jukebox Retro

Este arquivo contém exemplos de como usar o Jukebox Retro.

## 🎵 Início Rápido

### 1. Executar a Aplicação

```bash
# No terminal (Linux/macOS)
python3 jukebox_retro.py

# No prompt de comando (Windows)
python jukebox_retro.py
```

### 2. Adicionar Suas Primeiras Músicas

**Opção A: Adicionar arquivos individuais**
1. Clique no botão "➕ ADD MUSIC"
2. Navegue até sua pasta de músicas
3. Selecione uma ou mais músicas (use Ctrl/Cmd para múltipla seleção)
4. Clique em "Abrir"

**Opção B: Adicionar uma pasta inteira**
1. Clique no botão "📁 ADD FOLDER"
2. Selecione a pasta contendo suas músicas
3. Todas as músicas serão adicionadas automaticamente

### 3. Reproduzir Música

**Opção A: Double-click**
- Dê um double-click em qualquer música na playlist

**Opção B: Usar controles**
1. Selecione uma música
2. Clique no botão "▶ PLAY"

### 4. Controlar a Reprodução

- **⏸ PAUSE**: Pausa a música atual
- **▶ PLAY**: Retoma a reprodução
- **⏹ STOP**: Para completamente a reprodução
- **⏮ PREV**: Volta para a música anterior
- **NEXT ⏭**: Avança para a próxima música

### 5. Ajustar Volume

Use o controle deslizante "VOLUME" para ajustar o volume de 0 a 100.

## 📂 Organização Recomendada

Organize suas músicas assim para melhor experiência:

```
Minha Música/
├── Rock/
│   ├── banda1/
│   │   ├── 01 - música1.mp3
│   │   └── 02 - música2.mp3
│   └── banda2/
├── Jazz/
├── Eletrônica/
└── Favoritas/
```

## 🎨 Personalizando

### Modificar Cores da Interface

Edite as variáveis de cor no arquivo `jukebox_retro.py`:

```python
bg_color = "#2a2a2a"      # Cor de fundo
fg_color = "#00ff00"      # Cor do texto (verde fosforescente)
button_color = "#1a1a1a"  # Cor dos botões
```

Cores retro sugeridas:
- Verde clássico: `#00ff00`
- Âmbar: `#ffb000`
- Ciano: `#00ffff`
- Roxo: `#ff00ff`

## 💡 Dicas e Truques

### 1. Playlists Temáticas

Crie diferentes pastas para diferentes ocasiões:
- `~/Music/Trabalho/` - Música focada
- `~/Music/Festa/` - Música animada
- `~/Music/Relaxamento/` - Música calma

### 2. Atalho para Iniciar

**Linux:**
Adicione ao menu de aplicações ou crie um alias no `.bashrc`:
```bash
alias jukebox='cd ~/Jukebox-Retro && python3 jukebox_retro.py &'
```

**Windows:**
Crie um atalho no desktop apontando para:
```
C:\Python\python.exe C:\caminho\para\jukebox_retro.py
```

### 3. Auto-Iniciar com o Sistema

**Linux (systemd):**
Crie `~/.config/systemd/user/jukebox.service`:
```ini
[Unit]
Description=Jukebox Retro

[Service]
ExecStart=/usr/bin/python3 /caminho/completo/jukebox_retro.py
Restart=on-failure

[Install]
WantedBy=default.target
```

Habilite:
```bash
systemctl --user enable jukebox
systemctl --user start jukebox
```

### 4. Backup da Playlist

Sua playlist é salva em: `~/.jukebox_retro/config.json`

Para fazer backup:
```bash
# Linux/macOS
cp ~/.jukebox_retro/config.json ~/backup_playlist.json

# Windows
copy %USERPROFILE%\.jukebox_retro\config.json backup_playlist.json
```

### 5. Formatos de Áudio Recomendados

- **MP3**: Melhor compatibilidade, bom tamanho
- **FLAC**: Qualidade sem perda (arquivos maiores)
- **OGG**: Alternativa open-source ao MP3
- **WAV**: Qualidade máxima (arquivos muito grandes)

## 🔍 Casos de Uso

### Caso 1: DJ em Festa

```python
# Adicione sua pasta de música de festa
1. ADD FOLDER → Selecione "~/Music/Festa"
2. Ajuste volume para 80-90%
3. Deixe tocar automaticamente
```

### Caso 2: Música de Fundo para Trabalho

```python
# Adicione música instrumental ou calma
1. ADD FOLDER → Selecione "~/Music/Instrumental"
2. Ajuste volume para 30-40%
3. Minimize a janela
```

### Caso 3: Estudo de Álbum

```python
# Adicione apenas um álbum específico
1. ADD FOLDER → Selecione pasta do álbum
2. Dê play na primeira faixa
3. Deixe tocar em ordem
```

## 🐛 Solução de Problemas Comuns

### A música pula ou corta

- Verifique se o arquivo não está corrompido
- Tente converter para outro formato
- Reduza a qualidade do arquivo

### Metadados errados

Os metadados vêm dos arquivos. Para corrigir:
1. Use um editor de tags como Mp3tag (Windows) ou EasyTAG (Linux)
2. Atualize as informações
3. Recarregue a música no Jukebox

### Playlist não salva

Verifique permissões:
```bash
# Linux/macOS
ls -la ~/.jukebox_retro/
chmod 755 ~/.jukebox_retro/
```

## 📊 Estatísticas

O Jukebox Retro mantém registros em `~/.jukebox_retro/config.json`:
- Histórico de playlist
- Configurações de volume
- (Futuramente: contador de reproduções, favoritas, etc)

## 🎯 Próximos Passos

1. Explore todas as músicas da sua biblioteca
2. Organize em playlists temáticas
3. Experimente diferentes esquemas de cor
4. Contribua com feedback e sugestões!

---

**Divirta-se com seu Jukebox Retro!** 🎵🎉
