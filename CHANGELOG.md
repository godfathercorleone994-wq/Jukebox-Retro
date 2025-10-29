# Changelog

All notable changes to the Jukebox Retro project will be documented in this file.

## [1.0.0] - 2025-10-29

### Added
- Initial release of Jukebox Retro
- Cross-platform desktop music player (Windows and Linux)
- Retro-style GUI with green/orange phosphor terminal aesthetics
- Support for MP3, WAV, OGG, and FLAC audio formats
- Playlist management with automatic metadata extraction
- Add individual music files or entire folders
- Full playback controls:
  - Play/Pause
  - Stop
  - Next track
  - Previous track
  - Volume control
- Automatic advancement to next track
- Persistent playlist and settings storage
- Double-click to play tracks from playlist
- PyInstaller configuration for creating standalone executables
- Build scripts for Windows and Linux
- Comprehensive documentation (README.md and INSTALL.md)
- Basic unit tests
- Cross-platform compatibility

### Features
- **Offline First**: Works completely offline without internet connection
- **Auto-Save**: Automatically saves playlist and settings between sessions
- **Metadata Display**: Shows artist, title, album information
- **Time Display**: Shows current position and total duration
- **Retro Design**: Classic green terminal aesthetic with 3D buttons

### Technical
- Python 3.8+ support
- Tkinter for GUI (bundled with Python)
- Pygame for audio playback
- Mutagen for metadata extraction
- PyInstaller for creating installers
