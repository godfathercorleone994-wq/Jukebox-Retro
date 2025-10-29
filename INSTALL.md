# Guia de Instalação - Jukebox Retro

Este guia detalha como instalar e executar o Jukebox Retro em diferentes sistemas operacionais.

## 📋 Pré-requisitos

### Windows
- Windows 7 ou superior
- Python 3.8 ou superior (baixe de [python.org](https://www.python.org/downloads/))
  - **IMPORTANTE:** Durante a instalação do Python, marque a opção "Add Python to PATH"

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk
```

### Linux (Fedora/RHEL)
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

### Linux (Arch)
```bash
sudo pacman -S python python-pip tk
```

## 🚀 Instalação e Execução

### Método 1: Executar a partir do código fonte (Recomendado para desenvolvedores)

1. **Clone ou baixe o repositório:**
```bash
git clone https://github.com/godfathercorleone994-wq/Jukebox-Retro.git
cd Jukebox-Retro
```

Ou baixe o ZIP e extraia.

2. **Instale as dependências:**

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux:**
```bash
pip3 install -r requirements.txt
```

3. **Execute a aplicação:**

**Windows:**
```bash
python jukebox_retro.py
```

**Linux:**
```bash
python3 jukebox_retro.py
```

### Método 2: Criar executável standalone (Instalador)

Este método cria um arquivo executável que pode ser distribuído sem precisar instalar Python.

#### Windows

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Execute o script de build:**
```bash
build_windows.bat
```

3. **O executável será criado em:**
```
dist\JukeboxRetro.exe
```

4. **Distribua o executável:**
   - Você pode copiar o arquivo `JukeboxRetro.exe` para qualquer computador Windows
   - Não é necessário instalar Python no computador de destino
   - Double-click para executar

#### Linux

1. **Instale as dependências:**
```bash
pip3 install -r requirements.txt
```

2. **Torne o script executável e execute:**
```bash
chmod +x build_linux.sh
./build_linux.sh
```

3. **O executável será criado em:**
```
dist/JukeboxRetro
```

4. **Execute:**
```bash
./dist/JukeboxRetro
```

5. **Opcional - Criar um launcher de desktop:**

Crie o arquivo `~/.local/share/applications/jukebox-retro.desktop`:
```desktop
[Desktop Entry]
Type=Application
Name=Jukebox Retro
Comment=Retro music player
Exec=/caminho/completo/para/dist/JukeboxRetro
Icon=multimedia-player
Terminal=false
Categories=AudioVideo;Audio;Player;
```

Substitua `/caminho/completo/para/dist/JukeboxRetro` pelo caminho real do executável.

## 🎵 Primeiro Uso

1. **Inicie o Jukebox Retro**

2. **Adicione músicas:**
   - Clique em "➕ ADD MUSIC" para adicionar arquivos individuais
   - Clique em "📁 ADD FOLDER" para adicionar uma pasta inteira de músicas

3. **Comece a ouvir:**
   - Double-click em uma música para tocá-la
   - Use os controles de reprodução (Play, Pause, Stop, Next, Previous)
   - Ajuste o volume com o controle deslizante

## 🔧 Solução de Problemas

### Windows: "Python não é reconhecido como um comando interno"
- Reinstale o Python e marque "Add Python to PATH"
- Ou adicione manualmente o Python ao PATH do sistema

### Windows: Erro ao importar tkinter
- Reinstale o Python e certifique-se de que a opção "tcl/tk and IDLE" está marcada

### Linux: ModuleNotFoundError: No module named 'tkinter'
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Linux: Sem som ou erro de áudio
```bash
# Instale as dependências de áudio do pygame
sudo apt-get install python3-pygame libsdl2-mixer-2.0-0
```

### A música não toca
- Verifique se o arquivo está em um formato suportado (MP3, WAV, OGG, FLAC)
- Verifique se o arquivo não está corrompido
- Tente aumentar o volume
- Verifique se o sistema de som está funcionando

### PyInstaller não encontrado
```bash
pip install pyinstaller
# ou
pip3 install pyinstaller
```

## 📱 Criando Atalho no Desktop

### Windows

1. Navegue até `dist\JukeboxRetro.exe`
2. Clique com botão direito → Enviar para → Área de trabalho (criar atalho)

### Linux (GNOME/KDE)

1. Crie um arquivo `.desktop` como descrito acima
2. Ou simplesmente arraste o executável para a área de trabalho

## 🔄 Atualizações

Para atualizar para a versão mais recente:

```bash
cd Jukebox-Retro
git pull
pip install -r requirements.txt --upgrade
```

Depois recrie o executável se necessário.

## 💡 Dicas

1. **Atalhos de teclado:** Atualmente não implementados, mas planejados para versão futura
2. **Backup da playlist:** A playlist é salva em `~/.jukebox_retro/config.json`
3. **Formatos recomendados:** MP3 e FLAC para melhor qualidade
4. **Organização:** Use nomes de arquivos organizados para melhor exibição

## 🆘 Precisa de Ajuda?

- Abra uma issue no GitHub
- Verifique se há atualizações disponíveis
- Consulte o README.md para mais informações
