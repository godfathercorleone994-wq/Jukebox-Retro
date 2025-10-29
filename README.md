# Jukebox Retro 🎵

Uma aplicação de jukebox estilo retrô que funciona em Windows e Linux. Um player de música desktop com visual retrô, instalador nativo e funciona completamente offline.

## 📋 Características

- ✅ Aplicação desktop nativa (não é aplicação web)
- ✅ Funciona em Windows e Linux
- ✅ Interface visual estilo retrô (verde e laranja fosforescente)
- ✅ Reproduz músicas em formato MP3, WAV, OGG e FLAC
- ✅ Sistema para adicionar músicas individualmente ou pastas inteiras
- ✅ Gerenciamento de playlist
- ✅ Funciona completamente offline
- ✅ Salva automaticamente a playlist e configurações
- ✅ Controles: Play/Pause, Stop, Próxima, Anterior
- ✅ Controle de volume
- ✅ Exibe metadados das músicas (artista, título, álbum)
- ✅ Reprodução automática da próxima música

## 🖥️ Requisitos do Sistema

### Windows
- Windows 7 ou superior
- Python 3.8+ (para desenvolvimento)

### Linux
- Qualquer distribuição moderna
- Python 3.8+
- Dependências de áudio: `python3-pygame` ou `SDL2`

## 🚀 Instalação

### Opção 1: Executar a partir do código fonte

1. **Clone o repositório:**
```bash
git clone https://github.com/godfathercorleone994-wq/Jukebox-Retro.git
cd Jukebox-Retro
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
python jukebox_retro.py
```

### Opção 2: Criar instalador com PyInstaller

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Gere o executável:**

**Para Windows:**
```bash
pyinstaller jukebox_retro.spec
```

**Para Linux:**
```bash
pyinstaller jukebox_retro.spec
```

3. **O executável estará em:**
- `dist/JukeboxRetro.exe` (Windows)
- `dist/JukeboxRetro` (Linux)

## 📖 Como Usar

### Adicionar Músicas

1. **Adicionar arquivos individuais:**
   - Clique no botão "➕ ADD MUSIC"
   - Selecione um ou mais arquivos de música
   - Os arquivos serão adicionados à playlist

2. **Adicionar pasta inteira:**
   - Clique no botão "📁 ADD FOLDER"
   - Selecione uma pasta contendo músicas
   - Todas as músicas da pasta (e subpastas) serão adicionadas

### Controles de Reprodução

- **▶ PLAY/PAUSE:** Inicia ou pausa a reprodução
- **⏹ STOP:** Para a reprodução
- **⏮ PREV:** Volta para a música anterior
- **NEXT ⏭:** Avança para a próxima música
- **Double-click:** Clique duplo em uma música na playlist para tocá-la
- **Volume:** Use o controle deslizante para ajustar o volume

### Gerenciar Playlist

- **🗑 CLEAR PLAYLIST:** Remove todas as músicas da playlist
- A playlist é salva automaticamente
- As configurações são mantidas entre sessões

## 🎨 Interface

A interface possui um visual retrô inspirado em terminais antigos:
- Fundo escuro (#2a2a2a)
- Texto verde fosforescente (#00ff00)
- Título laranja (#ff6600)
- Botões com borda 3D
- Fonte monoespaçada (Courier)

## 📂 Formatos Suportados

- MP3 (MPEG Audio Layer 3)
- WAV (Waveform Audio File Format)
- OGG (Ogg Vorbis)
- FLAC (Free Lossless Audio Codec)

## 🔧 Tecnologias Utilizadas

- **Python 3:** Linguagem de programação principal
- **Tkinter:** Interface gráfica (inclusa no Python)
- **Pygame:** Reprodução de áudio
- **Mutagen:** Leitura de metadados de arquivos de áudio
- **PyInstaller:** Criação de executáveis standalone

## 💾 Armazenamento de Dados

- Configurações e playlist são salvos em: `~/.jukebox_retro/config.json`
- Não modifica os arquivos de música originais
- Apenas armazena caminhos e metadados

## 🐛 Solução de Problemas

### Linux: Sem som
```bash
# Instale as dependências de áudio
sudo apt-get install python3-pygame libsdl2-mixer-2.0-0
```

### Windows: Erro ao executar
- Certifique-se de ter Python 3.8+ instalado
- Execute como administrador se necessário

### Música não toca
- Verifique se o arquivo está em um formato suportado
- Verifique se o arquivo não está corrompido
- Tente aumentar o volume

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novos recursos
- Enviar pull requests

## 👨‍💻 Autor

Desenvolvido com ❤️ para amantes de música retrô!
