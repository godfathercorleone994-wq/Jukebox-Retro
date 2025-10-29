# Arquitetura do Jukebox Retro

Este documento descreve a arquitetura e estrutura do projeto Jukebox Retro.

## 📐 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     JUKEBOX RETRO                            │
│                  (Desktop Application)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │          GUI Layer (Tkinter)           │
         │  ┌──────────────────────────────────┐  │
         │  │  Retro Visual Interface          │  │
         │  │  - Title Display                 │  │
         │  │  - Now Playing Panel             │  │
         │  │  - Control Buttons               │  │
         │  │  - Volume Slider                 │  │
         │  │  - Playlist Listbox              │  │
         │  │  - Action Buttons                │  │
         │  └──────────────────────────────────┘  │
         └────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────┐
    │        Application Logic Layer                   │
    │  ┌───────────────────────────────────────────┐  │
    │  │  JukeboxRetro Class                       │  │
    │  │  ┌─────────────────────────────────────┐  │  │
    │  │  │  State Management                   │  │  │
    │  │  │  - playlist: List[Dict]             │  │  │
    │  │  │  - current_track_index: int         │  │  │
    │  │  │  - is_playing: bool                 │  │  │
    │  │  │  - is_paused: bool                  │  │  │
    │  │  │  - volume: float                    │  │  │
    │  │  └─────────────────────────────────────┘  │  │
    │  │  ┌─────────────────────────────────────┐  │  │
    │  │  │  Playback Control                   │  │  │
    │  │  │  - play_pause()                     │  │  │
    │  │  │  - stop()                           │  │  │
    │  │  │  - next_track()                     │  │  │
    │  │  │  - previous_track()                 │  │  │
    │  │  │  - play_track(index)                │  │  │
    │  │  └─────────────────────────────────────┘  │  │
    │  │  ┌─────────────────────────────────────┐  │  │
    │  │  │  Playlist Management                │  │  │
    │  │  │  - add_music()                      │  │  │
    │  │  │  - add_folder()                     │  │  │
    │  │  │  - add_track_to_playlist()          │  │  │
    │  │  │  - clear_playlist()                 │  │  │
    │  │  └─────────────────────────────────────┘  │  │
    │  │  ┌─────────────────────────────────────┐  │  │
    │  │  │  Configuration                      │  │  │
    │  │  │  - save_config()                    │  │  │
    │  │  │  - load_config()                    │  │  │
    │  │  └─────────────────────────────────────┘  │  │
    │  └───────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │      External Libraries Layer          │
         ├────────────────────────────────────────┤
         │  Pygame Mixer                          │
         │  - Audio Playback Engine               │
         │  - Format Support (MP3, WAV, OGG)      │
         │  - Volume Control                      │
         │  - Playback State Monitoring           │
         ├────────────────────────────────────────┤
         │  Mutagen                               │
         │  - Metadata Extraction                 │
         │  - Title, Artist, Album                │
         │  - Duration Calculation                │
         ├────────────────────────────────────────┤
         │  Threading                             │
         │  - Background Playback Monitor         │
         │  - Auto-advance Detection              │
         └────────────────────────────────────────┘
                              │
                              ▼
            ┌──────────────────────────────┐
            │     File System Layer        │
            ├──────────────────────────────┤
            │  Local Music Files           │
            │  - MP3, WAV, OGG, FLAC       │
            ├──────────────────────────────┤
            │  Configuration Storage       │
            │  ~/.jukebox_retro/           │
            │  └── config.json             │
            └──────────────────────────────┘
```

## 🔄 Fluxo de Dados

### 1. Adicionar Música

```
User Action (Add Music Button)
    │
    ▼
File Dialog (Select Files/Folder)
    │
    ▼
For Each File:
    │
    ├──> Extract Metadata (Mutagen)
    │       │
    │       ├──> Title
    │       ├──> Artist
    │       ├──> Album
    │       └──> Duration
    │
    ├──> Create Track Info Dict
    │
    └──> Add to Playlist
         │
         ▼
Update GUI Listbox
         │
         ▼
Save Configuration (config.json)
```

### 2. Reproduzir Música

```
User Action (Play Button / Double-click)
    │
    ▼
Get Track from Playlist[index]
    │
    ▼
Load Audio File (Pygame)
    │
    ▼
Start Playback
    │
    ▼
Update GUI State
    │   ├──> Update "Now Playing"
    │   ├──> Change Button Text
    │   └──> Highlight Track
    │
    ▼
Monitor Thread Detects Playback
    │
    ├──> Update Time Display
    │
    └──> When Track Ends
         │
         ▼
    Auto-advance to Next Track
```

### 3. Persistência de Configuração

```
Application Startup
    │
    ▼
Load config.json
    │
    ├──> Restore Playlist
    ├──> Restore Volume
    └──> Update GUI
         │
         ▼
User Interactions
    │
    ├──> Add/Remove Music
    ├──> Change Volume
    └──> [Changes Made]
         │
         ▼
Auto-save on Changes
    │
    ▼
Write config.json
```

## 🧩 Componentes Principais

### 1. JukeboxRetro Class
**Responsabilidade**: Classe principal que gerencia toda a aplicação

**Métodos Principais**:
- `__init__(root)`: Inicializa a aplicação
- `setup_gui()`: Cria a interface gráfica
- `play_track(index)`: Reproduz uma música
- `add_music()`: Adiciona arquivos de música
- `monitor_playback()`: Monitora estado de reprodução

### 2. GUI Components
**Responsabilidade**: Interface visual retro

**Elementos**:
- Title Frame: Logo/título da aplicação
- Now Playing Frame: Informações da música atual
- Control Frame: Botões de controle
- Volume Frame: Controle de volume
- Playlist Frame: Lista de músicas
- Action Frame: Botões de ação

### 3. Playback Engine (Pygame)
**Responsabilidade**: Reprodução de áudio

**Funcionalidades**:
- Carregamento de arquivos
- Play/Pause/Stop
- Controle de volume
- Monitoramento de estado

### 4. Metadata Extractor (Mutagen)
**Responsabilidade**: Extração de metadados

**Informações Extraídas**:
- Título da música
- Nome do artista
- Nome do álbum
- Duração

### 5. Configuration Manager
**Responsabilidade**: Persistência de dados

**Arquivo**: `~/.jukebox_retro/config.json`

**Conteúdo**:
```json
{
  "playlist": [
    {
      "path": "/path/to/music.mp3",
      "title": "Song Title",
      "artist": "Artist Name",
      "album": "Album Name",
      "duration": 180
    }
  ],
  "volume": 0.7
}
```

## 🎨 Design Patterns

### 1. Observer Pattern (Implicit)
- Monitor thread observa estado de reprodução
- GUI atualiza quando estado muda

### 2. Singleton Pattern (Implicit)
- Apenas uma instância da aplicação

### 3. Model-View-Controller (MVC-like)
- **Model**: Playlist data, configuration
- **View**: Tkinter GUI components
- **Controller**: JukeboxRetro class methods

## 🔧 Tecnologias e Dependências

```
┌─────────────────────────────────────┐
│         Python 3.8+                 │
├─────────────────────────────────────┤
│  Tkinter (GUI) - Built-in           │
│  Pygame (Audio) - pip install       │
│  Mutagen (Metadata) - pip install   │
└─────────────────────────────────────┘
```

## 🚀 Build e Deploy

### Desenvolvimento
```bash
python jukebox_retro.py
```

### Produção (Standalone)
```bash
pyinstaller jukebox_retro.spec

# Gera:
# dist/JukeboxRetro.exe (Windows)
# dist/JukeboxRetro (Linux)
```

## 📊 Estatísticas do Código

- **Total de Linhas**: 479
- **Classes**: 1 (JukeboxRetro)
- **Métodos**: ~20
- **Threads**: 2 (Main + Monitor)
- **Dependências Externas**: 3 (pygame, mutagen, pyinstaller)

## 🔐 Segurança

- ✅ Sem chamadas de rede (exceto ao adicionar músicas de fontes de rede)
- ✅ Sem coleta de dados
- ✅ Armazenamento local apenas
- ✅ Sem bibliotecas com vulnerabilidades conhecidas
- ✅ CodeQL: 0 alertas de segurança

## 🎯 Características Técnicas

- **Cross-platform**: Python + Tkinter
- **Threading**: Monitor assíncrono de reprodução
- **Event-driven**: GUI baseada em eventos Tkinter
- **Persistent Storage**: JSON configuration
- **Error Handling**: Try-catch em operações críticas
- **Memory Efficient**: Streaming de áudio via Pygame

---

Esta arquitetura garante:
- ✅ Manutenibilidade
- ✅ Extensibilidade
- ✅ Performance
- ✅ Cross-platform compatibility
- ✅ User-friendly interface
