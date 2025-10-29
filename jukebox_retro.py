#!/usr/bin/env python3
"""
Jukebox Retro - A retro-style music player for Windows and Linux
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import os
import json
from pathlib import Path
from mutagen import File as MutagenFile
from typing import List, Dict, Optional
import threading
import time


class JukeboxRetro:
    """Main Jukebox application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Jukebox Retro")
        self.root.geometry("800x600")
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Application state
        self.playlist: List[Dict] = []
        self.current_track_index: int = -1
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.volume: float = 0.7
        
        # Config file path
        self.config_file = Path.home() / ".jukebox_retro" / "config.json"
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load saved configuration
        self.load_config()
        
        # Setup GUI
        self.setup_gui()
        
        # Start playback monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_playback, daemon=True)
        self.monitor_thread.start()
        
    def setup_gui(self):
        """Setup the retro-style GUI"""
        # Set retro color scheme
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        self.root.configure(bg=bg_color)
        
        # Title Label
        title_frame = tk.Frame(self.root, bg=bg_color)
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="♪ JUKEBOX RETRO ♪",
            font=("Courier", 24, "bold"),
            fg="#ff6600",
            bg=bg_color
        )
        title_label.pack()
        
        # Now Playing Display
        self.now_playing_frame = tk.Frame(self.root, bg=button_color, relief=tk.SUNKEN, bd=3)
        self.now_playing_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            self.now_playing_frame,
            text="NOW PLAYING:",
            font=("Courier", 10, "bold"),
            fg=fg_color,
            bg=button_color
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.now_playing_label = tk.Label(
            self.now_playing_frame,
            text="No track loaded",
            font=("Courier", 14),
            fg="#ffffff",
            bg=button_color,
            wraplength=700
        )
        self.now_playing_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        self.time_label = tk.Label(
            self.now_playing_frame,
            text="00:00 / 00:00",
            font=("Courier", 10),
            fg=fg_color,
            bg=button_color
        )
        self.time_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Control Buttons
        control_frame = tk.Frame(self.root, bg=bg_color)
        control_frame.pack(pady=10)
        
        button_style = {
            "font": ("Courier", 12, "bold"),
            "bg": button_color,
            "fg": fg_color,
            "activebackground": "#333333",
            "activeforeground": "#00ff00",
            "width": 8,
            "relief": tk.RAISED,
            "bd": 3
        }
        
        self.prev_button = tk.Button(control_frame, text="⏮ PREV", command=self.previous_track, **button_style)
        self.prev_button.grid(row=0, column=0, padx=5)
        
        self.play_button = tk.Button(control_frame, text="▶ PLAY", command=self.play_pause, **button_style)
        self.play_button.grid(row=0, column=1, padx=5)
        
        self.stop_button = tk.Button(control_frame, text="⏹ STOP", command=self.stop, **button_style)
        self.stop_button.grid(row=0, column=2, padx=5)
        
        self.next_button = tk.Button(control_frame, text="NEXT ⏭", command=self.next_track, **button_style)
        self.next_button.grid(row=0, column=3, padx=5)
        
        # Volume Control
        volume_frame = tk.Frame(self.root, bg=bg_color)
        volume_frame.pack(pady=10)
        
        tk.Label(
            volume_frame,
            text="VOLUME:",
            font=("Courier", 10, "bold"),
            fg=fg_color,
            bg=bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.volume_scale = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.change_volume,
            bg=button_color,
            fg=fg_color,
            highlightbackground=bg_color,
            troughcolor="#444444",
            length=200
        )
        self.volume_scale.set(int(self.volume * 100))
        self.volume_scale.pack(side=tk.LEFT)
        
        # Playlist Frame
        playlist_label_frame = tk.Frame(self.root, bg=bg_color)
        playlist_label_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            playlist_label_frame,
            text="PLAYLIST:",
            font=("Courier", 12, "bold"),
            fg=fg_color,
            bg=bg_color
        ).pack(side=tk.LEFT)
        
        # Playlist Listbox with Scrollbar
        list_frame = tk.Frame(self.root, bg=bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_box = tk.Listbox(
            list_frame,
            font=("Courier", 10),
            bg=button_color,
            fg="#ffffff",
            selectbackground="#00ff00",
            selectforeground="#000000",
            yscrollcommand=scrollbar.set,
            relief=tk.SUNKEN,
            bd=3
        )
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.playlist_box.bind('<Double-Button-1>', self.on_playlist_double_click)
        
        scrollbar.config(command=self.playlist_box.yview)
        
        # Action Buttons
        action_frame = tk.Frame(self.root, bg=bg_color)
        action_frame.pack(pady=10)
        
        action_button_style = {
            "font": ("Courier", 10, "bold"),
            "bg": button_color,
            "fg": fg_color,
            "activebackground": "#333333",
            "activeforeground": "#00ff00",
            "width": 15,
            "relief": tk.RAISED,
            "bd": 3
        }
        
        tk.Button(
            action_frame,
            text="➕ ADD MUSIC",
            command=self.add_music,
            **action_button_style
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            action_frame,
            text="📁 ADD FOLDER",
            command=self.add_folder,
            **action_button_style
        ).grid(row=0, column=1, padx=5)
        
        tk.Button(
            action_frame,
            text="🗑 CLEAR PLAYLIST",
            command=self.clear_playlist,
            **action_button_style
        ).grid(row=0, column=2, padx=5)
        
    def add_music(self):
        """Add individual music files to playlist"""
        files = filedialog.askopenfilenames(
            title="Select Music Files",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.flac"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("OGG Files", "*.ogg"),
                ("FLAC Files", "*.flac"),
                ("All Files", "*.*")
            ]
        )
        
        if files:
            for file in files:
                self.add_track_to_playlist(file)
            self.save_config()
            
    def add_folder(self):
        """Add all music files from a folder"""
        folder = filedialog.askdirectory(title="Select Music Folder")
        
        if folder:
            audio_extensions = ['.mp3', '.wav', '.ogg', '.flac']
            found_files = 0
            
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in audio_extensions):
                        file_path = os.path.join(root, file)
                        self.add_track_to_playlist(file_path)
                        found_files += 1
            
            if found_files > 0:
                messagebox.showinfo("Success", f"Added {found_files} music files to playlist!")
                self.save_config()
            else:
                messagebox.showwarning("No Files", "No audio files found in the selected folder.")
    
    def add_track_to_playlist(self, file_path: str):
        """Add a track to the playlist with metadata"""
        if not os.path.exists(file_path):
            return
        
        # Extract metadata
        metadata = self.get_metadata(file_path)
        
        track_info = {
            'path': file_path,
            'title': metadata.get('title', os.path.basename(file_path)),
            'artist': metadata.get('artist', 'Unknown Artist'),
            'album': metadata.get('album', 'Unknown Album'),
            'duration': metadata.get('duration', 0)
        }
        
        self.playlist.append(track_info)
        
        # Update listbox
        display_text = f"{track_info['artist']} - {track_info['title']}"
        self.playlist_box.insert(tk.END, display_text)
    
    def get_metadata(self, file_path: str) -> Dict:
        """Extract metadata from audio file"""
        metadata = {}
        
        try:
            audio = MutagenFile(file_path, easy=True)
            if audio is not None:
                metadata['title'] = audio.get('title', [os.path.basename(file_path)])[0] if 'title' in audio else os.path.basename(file_path)
                metadata['artist'] = audio.get('artist', ['Unknown Artist'])[0] if 'artist' in audio else 'Unknown Artist'
                metadata['album'] = audio.get('album', ['Unknown Album'])[0] if 'album' in audio else 'Unknown Album'
                
                # Get duration
                if hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                    metadata['duration'] = int(audio.info.length)
        except Exception as e:
            print(f"Error reading metadata from {file_path}: {e}")
        
        return metadata
    
    def clear_playlist(self):
        """Clear the entire playlist"""
        if messagebox.askyesno("Clear Playlist", "Are you sure you want to clear the playlist?"):
            self.stop()
            self.playlist.clear()
            self.playlist_box.delete(0, tk.END)
            self.current_track_index = -1
            self.now_playing_label.config(text="No track loaded")
            self.time_label.config(text="00:00 / 00:00")
            self.save_config()
    
    def play_pause(self):
        """Play or pause the current track"""
        if not self.playlist:
            messagebox.showwarning("Empty Playlist", "Please add music to the playlist first!")
            return
        
        if self.is_paused:
            # Resume playback
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_button.config(text="⏸ PAUSE")
        elif self.is_playing:
            # Pause playback
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="▶ PLAY")
        else:
            # Start playback
            if self.current_track_index == -1:
                self.current_track_index = 0
            
            self.play_track(self.current_track_index)
    
    def play_track(self, index: int):
        """Play a specific track from the playlist"""
        if 0 <= index < len(self.playlist):
            track = self.playlist[index]
            
            try:
                pygame.mixer.music.load(track['path'])
                pygame.mixer.music.play()
                
                self.current_track_index = index
                self.is_playing = True
                self.is_paused = False
                
                # Update UI
                self.now_playing_label.config(
                    text=f"{track['artist']} - {track['title']}\nAlbum: {track['album']}"
                )
                self.play_button.config(text="⏸ PAUSE")
                
                # Highlight current track
                self.playlist_box.selection_clear(0, tk.END)
                self.playlist_box.selection_set(index)
                self.playlist_box.see(index)
                
            except Exception as e:
                messagebox.showerror("Playback Error", f"Could not play track:\n{str(e)}")
    
    def stop(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_button.config(text="▶ PLAY")
    
    def next_track(self):
        """Play the next track in the playlist"""
        if not self.playlist:
            return
        
        next_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_track(next_index)
    
    def previous_track(self):
        """Play the previous track in the playlist"""
        if not self.playlist:
            return
        
        prev_index = (self.current_track_index - 1) % len(self.playlist)
        self.play_track(prev_index)
    
    def on_playlist_double_click(self, event):
        """Handle double-click on playlist item"""
        selection = self.playlist_box.curselection()
        if selection:
            self.play_track(selection[0])
    
    def change_volume(self, value):
        """Change the volume"""
        self.volume = int(value) / 100
        pygame.mixer.music.set_volume(self.volume)
    
    def monitor_playback(self):
        """Monitor playback and auto-play next track"""
        while True:
            if self.is_playing and not self.is_paused:
                if not pygame.mixer.music.get_busy():
                    # Track finished, play next
                    self.root.after(0, self.next_track)
                    time.sleep(1)
                else:
                    # Update time display
                    if self.current_track_index >= 0:
                        try:
                            pos = pygame.mixer.music.get_pos() / 1000
                            duration = self.playlist[self.current_track_index].get('duration', 0)
                            time_str = f"{self.format_time(int(pos))} / {self.format_time(duration)}"
                            self.root.after(0, lambda: self.time_label.config(text=time_str))
                        except:
                            pass
            
            time.sleep(0.5)
    
    def format_time(self, seconds: int) -> str:
        """Format seconds to MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def save_config(self):
        """Save playlist and settings to config file"""
        config = {
            'playlist': self.playlist,
            'volume': self.volume
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_config(self):
        """Load playlist and settings from config file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.playlist = config.get('playlist', [])
                self.volume = config.get('volume', 0.7)
                
                # Restore playlist in GUI
                for track in self.playlist:
                    display_text = f"{track['artist']} - {track['title']}"
                    self.playlist_box.insert(tk.END, display_text)
                
            except Exception as e:
                print(f"Error loading config: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JukeboxRetro(root)
    
    # Handle window close
    def on_closing():
        app.stop()
        app.save_config()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
