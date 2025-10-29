#!/usr/bin/env python3
"""
Jukebox Retro - A retro-style music player for Windows and Linux
With integrated payment system and administration features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pygame
import os
import json
from pathlib import Path
from mutagen import File as MutagenFile
from typing import List, Dict, Optional
import threading
import time
import uuid
from datetime import datetime
from models import (
    DataStore, User, Transaction, UsageRecord, CashRegister,
    PaymentMethod, UserRole
)


class JukeboxRetro:
    """Main Jukebox application class with payment system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Jukebox Retro")
        self.root.geometry("1000x700")
        
        # Initialize data store
        self.data_store = DataStore()
        
        # Current user
        self.current_user: Optional[User] = None
        
        # Song cost configuration
        self.song_cost = 1.0  # Cost per song in credits/currency
        
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
        
        # Show login dialog first
        self.show_login_dialog()
        
        if self.current_user is None:
            # User cancelled login
            self.root.destroy()
            return
        
        # Load saved configuration
        self.load_config()
        
        # Setup GUI
        self.setup_gui()
        
        # Start playback monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_playback, daemon=True)
        self.monitor_thread.start()
    
    def show_login_dialog(self):
        """Show login dialog for user authentication"""
        login_window = tk.Toplevel(self.root)
        login_window.title("Login - Jukebox Retro")
        login_window.geometry("400x300")
        login_window.transient(self.root)
        login_window.grab_set()
        
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        login_window.configure(bg=bg_color)
        
        # Center the window
        login_window.update_idletasks()
        width = login_window.winfo_width()
        height = login_window.winfo_height()
        x = (login_window.winfo_screenwidth() // 2) - (width // 2)
        y = (login_window.winfo_screenheight() // 2) - (height // 2)
        login_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Title
        tk.Label(
            login_window,
            text="♪ JUKEBOX LOGIN ♪",
            font=("Courier", 18, "bold"),
            fg="#ff6600",
            bg=bg_color
        ).pack(pady=20)
        
        # Username
        tk.Label(
            login_window,
            text="Username:",
            font=("Courier", 12),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=(10, 0))
        
        username_entry = tk.Entry(
            login_window,
            font=("Courier", 12),
            bg=button_color,
            fg="#ffffff",
            insertbackground="#00ff00"
        )
        username_entry.pack(pady=5)
        username_entry.focus()
        
        # Password
        tk.Label(
            login_window,
            text="Password:",
            font=("Courier", 12),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=(10, 0))
        
        password_entry = tk.Entry(
            login_window,
            font=("Courier", 12),
            bg=button_color,
            fg="#ffffff",
            insertbackground="#00ff00",
            show="*"
        )
        password_entry.pack(pady=5)
        
        # Info label
        info_label = tk.Label(
            login_window,
            text="Default: admin / admin123",
            font=("Courier", 8),
            fg="#888888",
            bg=bg_color
        )
        info_label.pack(pady=5)
        
        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password", parent=login_window)
                return
            
            user = self.data_store.get_user(username)
            
            if user and self.data_store.verify_password(password, user.password_hash):
                self.current_user = user
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=login_window)
        
        def on_cancel():
            self.current_user = None
            login_window.destroy()
        
        # Buttons
        button_frame = tk.Frame(login_window, bg=bg_color)
        button_frame.pack(pady=20)
        
        button_style = {
            "font": ("Courier", 12, "bold"),
            "bg": button_color,
            "fg": fg_color,
            "activebackground": "#333333",
            "activeforeground": "#00ff00",
            "width": 10,
            "relief": tk.RAISED,
            "bd": 3
        }
        
        tk.Button(button_frame, text="LOGIN", command=do_login, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="CANCEL", command=on_cancel, **button_style).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        password_entry.bind('<Return>', lambda e: do_login())
        
        # Wait for the dialog to close
        login_window.wait_window()
    
    def setup_gui(self):
        """Setup the retro-style GUI with payment system"""
        # Set retro color scheme
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        self.root.configure(bg=bg_color)
        
        # Top bar with user info and admin button
        top_bar = tk.Frame(self.root, bg=bg_color)
        top_bar.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        # User info on the left
        user_info_text = f"👤 {self.current_user.username}"
        if self.current_user.is_admin():
            user_info_text += " [ADMIN]"
        user_info_text += f" | Créditos: R$ {self.current_user.credits:.2f}"
        
        self.user_info_label = tk.Label(
            top_bar,
            text=user_info_text,
            font=("Courier", 10, "bold"),
            fg=fg_color,
            bg=bg_color
        )
        self.user_info_label.pack(side=tk.LEFT)
        
        # Admin button on the right
        if self.current_user.is_admin():
            admin_button_style = {
                "font": ("Courier", 10, "bold"),
                "bg": "#cc0000",
                "fg": "#ffffff",
                "activebackground": "#ff0000",
                "activeforeground": "#ffffff",
                "width": 12,
                "relief": tk.RAISED,
                "bd": 3
            }
            tk.Button(
                top_bar,
                text="⚙ ADMIN",
                command=self.show_admin_panel,
                **admin_button_style
            ).pack(side=tk.RIGHT, padx=5)
        
        # Add credits button for all users
        add_credits_button_style = {
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
            top_bar,
            text="💰 ADD CRÉDITOS",
            command=self.add_credits_dialog,
            **add_credits_button_style
        ).pack(side=tk.RIGHT, padx=5)
        
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
        """Play or pause the current track with payment check"""
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
            # Start playback - check payment first
            if self.current_track_index == -1:
                self.current_track_index = 0
            
            # Check if user has enough credits or process payment
            if not self.process_payment_for_song():
                return
            
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
        self.current_track_index = next_index
        
        # Check payment before playing
        if not self.process_payment_for_song():
            self.stop()
            return
            
        self.play_track(next_index)
    
    def previous_track(self):
        """Play the previous track in the playlist"""
        if not self.playlist:
            return
        
        prev_index = (self.current_track_index - 1) % len(self.playlist)
        self.current_track_index = prev_index
        
        # Check payment before playing
        if not self.process_payment_for_song():
            self.stop()
            return
            
        self.play_track(prev_index)
    
    def on_playlist_double_click(self, event):
        """Handle double-click on playlist item"""
        selection = self.playlist_box.curselection()
        if selection:
            self.current_track_index = selection[0]
            if self.process_payment_for_song():
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
    
    def process_payment_for_song(self) -> bool:
        """Process payment for playing a song"""
        track = self.playlist[self.current_track_index]
        
        # Check if user has enough credits
        if self.current_user.credits >= self.song_cost:
            # Use credits
            payment_method = PaymentMethod.CREDITS.value
            self.current_user.credits -= self.song_cost
            self.data_store.update_user(self.current_user)
            self.update_user_info_display()
        else:
            # Show payment dialog
            payment_method = self.show_payment_dialog()
            if payment_method is None:
                messagebox.showwarning("Pagamento Cancelado", "Pagamento necessário para tocar música.")
                return False
        
        # Record transaction
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            username=self.current_user.username,
            payment_method=payment_method,
            amount=self.song_cost,
            description=f"Música: {track['artist']} - {track['title']}"
        )
        self.data_store.add_transaction(transaction)
        
        # Record cash register entry (income)
        if payment_method != PaymentMethod.CREDITS.value:
            cash_entry = CashRegister(
                entry_id=str(uuid.uuid4()),
                entry_type="income",
                amount=self.song_cost,
                payment_method=payment_method,
                description=f"Música: {track['title']}"
            )
            self.data_store.add_cash_register_entry(cash_entry)
        
        # Record usage statistics
        usage_record = UsageRecord(
            record_id=str(uuid.uuid4()),
            username=self.current_user.username,
            song_title=track['title'],
            song_artist=track['artist'],
            payment_method=payment_method,
            cost=self.song_cost
        )
        self.data_store.add_usage_record(usage_record)
        
        return True
    
    def show_payment_dialog(self) -> Optional[str]:
        """Show dialog for payment method selection"""
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Selecionar Método de Pagamento")
        payment_window.geometry("450x400")
        payment_window.transient(self.root)
        payment_window.grab_set()
        
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        payment_window.configure(bg=bg_color)
        
        # Center the window
        payment_window.update_idletasks()
        width = payment_window.winfo_width()
        height = payment_window.winfo_height()
        x = (payment_window.winfo_screenwidth() // 2) - (width // 2)
        y = (payment_window.winfo_screenheight() // 2) - (height // 2)
        payment_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Title
        tk.Label(
            payment_window,
            text="💳 PAGAMENTO",
            font=("Courier", 18, "bold"),
            fg="#ff6600",
            bg=bg_color
        ).pack(pady=20)
        
        # Amount
        tk.Label(
            payment_window,
            text=f"Valor: R$ {self.song_cost:.2f}",
            font=("Courier", 14, "bold"),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=10)
        
        selected_method = [None]
        
        def select_payment(method):
            selected_method[0] = method
            payment_window.destroy()
        
        # Payment buttons
        button_style = {
            "font": ("Courier", 12, "bold"),
            "bg": button_color,
            "fg": fg_color,
            "activebackground": "#333333",
            "activeforeground": "#00ff00",
            "width": 20,
            "relief": tk.RAISED,
            "bd": 3
        }
        
        tk.Button(
            payment_window,
            text="📱 PIX",
            command=lambda: select_payment(PaymentMethod.PIX.value),
            **button_style
        ).pack(pady=5)
        
        tk.Button(
            payment_window,
            text="💵 DINHEIRO",
            command=lambda: select_payment(PaymentMethod.CASH.value),
            **button_style
        ).pack(pady=5)
        
        tk.Button(
            payment_window,
            text="💳 DÉBITO",
            command=lambda: select_payment(PaymentMethod.DEBIT.value),
            **button_style
        ).pack(pady=5)
        
        tk.Button(
            payment_window,
            text="💳 CRÉDITO",
            command=lambda: select_payment(PaymentMethod.CREDIT.value),
            **button_style
        ).pack(pady=5)
        
        # Cancel button
        tk.Button(
            payment_window,
            text="❌ CANCELAR",
            command=lambda: payment_window.destroy(),
            bg="#cc0000",
            fg="#ffffff",
            font=("Courier", 12, "bold"),
            activebackground="#ff0000",
            width=20,
            relief=tk.RAISED,
            bd=3
        ).pack(pady=20)
        
        payment_window.wait_window()
        return selected_method[0]
    
    def add_credits_dialog(self):
        """Show dialog for adding credits"""
        add_credits_window = tk.Toplevel(self.root)
        add_credits_window.title("Adicionar Créditos")
        add_credits_window.geometry("450x450")
        add_credits_window.transient(self.root)
        add_credits_window.grab_set()
        
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        add_credits_window.configure(bg=bg_color)
        
        # Center the window
        add_credits_window.update_idletasks()
        width = add_credits_window.winfo_width()
        height = add_credits_window.winfo_height()
        x = (add_credits_window.winfo_screenwidth() // 2) - (width // 2)
        y = (add_credits_window.winfo_screenheight() // 2) - (height // 2)
        add_credits_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Title
        tk.Label(
            add_credits_window,
            text="💰 ADICIONAR CRÉDITOS",
            font=("Courier", 16, "bold"),
            fg="#ff6600",
            bg=bg_color
        ).pack(pady=20)
        
        # Current balance
        tk.Label(
            add_credits_window,
            text=f"Saldo Atual: R$ {self.current_user.credits:.2f}",
            font=("Courier", 12),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=10)
        
        # Amount input
        tk.Label(
            add_credits_window,
            text="Valor a adicionar:",
            font=("Courier", 12),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=(20, 5))
        
        amount_entry = tk.Entry(
            add_credits_window,
            font=("Courier", 14),
            bg=button_color,
            fg="#ffffff",
            insertbackground="#00ff00",
            width=15,
            justify=tk.CENTER
        )
        amount_entry.pack(pady=5)
        amount_entry.focus()
        
        def add_credits_with_payment(payment_method: str):
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError("Valor deve ser positivo")
                
                # Add credits to user
                self.current_user.credits += amount
                self.data_store.update_user(self.current_user)
                self.update_user_info_display()
                
                # Record transaction
                transaction = Transaction(
                    transaction_id=str(uuid.uuid4()),
                    username=self.current_user.username,
                    payment_method=payment_method,
                    amount=amount,
                    description="Recarga de créditos"
                )
                self.data_store.add_transaction(transaction)
                
                # Record cash register entry (income) - only if not admin adding for free
                if payment_method != PaymentMethod.ADMIN_FREE.value:
                    cash_entry = CashRegister(
                        entry_id=str(uuid.uuid4()),
                        entry_type="income",
                        amount=amount,
                        payment_method=payment_method,
                        description="Recarga de créditos"
                    )
                    self.data_store.add_cash_register_entry(cash_entry)
                
                messagebox.showinfo("Sucesso", f"R$ {amount:.2f} adicionados com sucesso!", parent=add_credits_window)
                add_credits_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Erro", f"Valor inválido: {str(e)}", parent=add_credits_window)
        
        # Payment buttons
        button_style = {
            "font": ("Courier", 11, "bold"),
            "bg": button_color,
            "fg": fg_color,
            "activebackground": "#333333",
            "activeforeground": "#00ff00",
            "width": 20,
            "relief": tk.RAISED,
            "bd": 3
        }
        
        if self.current_user.is_admin():
            tk.Button(
                add_credits_window,
                text="⭐ GRÁTIS (ADMIN)",
                command=lambda: add_credits_with_payment(PaymentMethod.ADMIN_FREE.value),
                bg="#cc00cc",
                fg="#ffffff",
                font=("Courier", 11, "bold"),
                activebackground="#ff00ff",
                width=20,
                relief=tk.RAISED,
                bd=3
            ).pack(pady=5)
        
        tk.Label(
            add_credits_window,
            text="Pagar com:",
            font=("Courier", 10),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=(10, 5))
        
        tk.Button(
            add_credits_window,
            text="📱 PIX",
            command=lambda: add_credits_with_payment(PaymentMethod.PIX.value),
            **button_style
        ).pack(pady=3)
        
        tk.Button(
            add_credits_window,
            text="💵 DINHEIRO",
            command=lambda: add_credits_with_payment(PaymentMethod.CASH.value),
            **button_style
        ).pack(pady=3)
        
        tk.Button(
            add_credits_window,
            text="💳 DÉBITO",
            command=lambda: add_credits_with_payment(PaymentMethod.DEBIT.value),
            **button_style
        ).pack(pady=3)
        
        tk.Button(
            add_credits_window,
            text="💳 CRÉDITO",
            command=lambda: add_credits_with_payment(PaymentMethod.CREDIT.value),
            **button_style
        ).pack(pady=3)
        
        # Cancel button
        tk.Button(
            add_credits_window,
            text="❌ CANCELAR",
            command=lambda: add_credits_window.destroy(),
            bg="#cc0000",
            fg="#ffffff",
            font=("Courier", 11, "bold"),
            activebackground="#ff0000",
            width=20,
            relief=tk.RAISED,
            bd=3
        ).pack(pady=15)
    
    def update_user_info_display(self):
        """Update user info label with current credits"""
        user_info_text = f"👤 {self.current_user.username}"
        if self.current_user.is_admin():
            user_info_text += " [ADMIN]"
        user_info_text += f" | Créditos: R$ {self.current_user.credits:.2f}"
        self.user_info_label.config(text=user_info_text)
    
    def show_admin_panel(self):
        """Show admin panel with statistics and cash register"""
        if not self.current_user.is_admin():
            messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar este painel.")
            return
        
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Painel de Administração")
        admin_window.geometry("900x700")
        admin_window.transient(self.root)
        
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        admin_window.configure(bg=bg_color)
        
        # Title
        tk.Label(
            admin_window,
            text="⚙ PAINEL DE ADMINISTRAÇÃO ⚙",
            font=("Courier", 18, "bold"),
            fg="#ff6600",
            bg=bg_color
        ).pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(admin_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Statistics
        stats_frame = tk.Frame(notebook, bg=bg_color)
        notebook.add(stats_frame, text="📊 Estatísticas")
        self.create_statistics_tab(stats_frame, bg_color, fg_color, button_color)
        
        # Tab 2: Cash Register
        cash_frame = tk.Frame(notebook, bg=bg_color)
        notebook.add(cash_frame, text="💰 Caixa")
        self.create_cash_register_tab(cash_frame, bg_color, fg_color, button_color)
        
        # Tab 3: Users
        users_frame = tk.Frame(notebook, bg=bg_color)
        notebook.add(users_frame, text="👥 Usuários")
        self.create_users_tab(users_frame, bg_color, fg_color, button_color)
        
        # Tab 4: Transactions
        transactions_frame = tk.Frame(notebook, bg=bg_color)
        notebook.add(transactions_frame, text="💳 Transações")
        self.create_transactions_tab(transactions_frame, bg_color, fg_color, button_color)
    
    def create_statistics_tab(self, parent, bg_color, fg_color, button_color):
        """Create statistics tab content"""
        # Load usage records
        usage_records = self.data_store.load_usage_records()
        
        # Calculate statistics
        total_songs = len(usage_records)
        total_revenue = sum(r.cost for r in usage_records)
        
        # Payment method breakdown
        payment_methods = {}
        for record in usage_records:
            pm = record.payment_method or "unknown"
            payment_methods[pm] = payment_methods.get(pm, 0) + 1
        
        # Top songs
        song_counts = {}
        for record in usage_records:
            key = f"{record.song_artist} - {record.song_title}"
            song_counts[key] = song_counts.get(key, 0) + 1
        
        top_songs = sorted(song_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Display statistics
        stats_text = tk.Text(
            parent,
            font=("Courier", 10),
            bg=button_color,
            fg="#ffffff",
            wrap=tk.WORD,
            height=30
        )
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add statistics content
        stats_content = f"""
╔══════════════════════════════════════════════════════════════╗
║              ESTATÍSTICAS DE USO - JUKEBOX RETRO             ║
╚══════════════════════════════════════════════════════════════╝

📊 RESUMO GERAL
────────────────────────────────────────────────────────────────
  Total de Músicas Tocadas: {total_songs}
  Receita Total: R$ {total_revenue:.2f}
  Custo por Música: R$ {self.song_cost:.2f}

💳 MÉTODOS DE PAGAMENTO
────────────────────────────────────────────────────────────────
"""
        for method, count in payment_methods.items():
            percentage = (count / total_songs * 100) if total_songs > 0 else 0
            stats_content += f"  {method.upper()}: {count} ({percentage:.1f}%)\n"
        
        stats_content += f"""
🎵 TOP 10 MÚSICAS MAIS TOCADAS
────────────────────────────────────────────────────────────────
"""
        for i, (song, count) in enumerate(top_songs, 1):
            stats_content += f"  {i}. {song} - {count}x\n"
        
        if not top_songs:
            stats_content += "  Nenhuma música tocada ainda.\n"
        
        stats_text.insert("1.0", stats_content)
        stats_text.config(state=tk.DISABLED)
    
    def create_cash_register_tab(self, parent, bg_color, fg_color, button_color):
        """Create cash register tab content"""
        # Get cash balance
        balance = self.data_store.get_cash_balance()
        
        # Load entries
        entries = self.data_store.load_cash_register()
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Balance display
        balance_frame = tk.Frame(parent, bg=bg_color)
        balance_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            balance_frame,
            text="💰 SALDO DO CAIXA 💰",
            font=("Courier", 14, "bold"),
            fg="#ff6600",
            bg=bg_color
        ).pack(pady=5)
        
        balance_text = f"""
Total Geral: R$ {balance['total']:.2f}

Por Método de Pagamento:
  PIX: R$ {balance.get(PaymentMethod.PIX.value, 0):.2f}
  Dinheiro: R$ {balance.get(PaymentMethod.CASH.value, 0):.2f}
  Débito: R$ {balance.get(PaymentMethod.DEBIT.value, 0):.2f}
  Crédito: R$ {balance.get(PaymentMethod.CREDIT.value, 0):.2f}
"""
        
        tk.Label(
            balance_frame,
            text=balance_text,
            font=("Courier", 10),
            fg=fg_color,
            bg=bg_color,
            justify=tk.LEFT
        ).pack()
        
        # Entries list
        tk.Label(
            parent,
            text="Últimas Movimentações:",
            font=("Courier", 12, "bold"),
            fg=fg_color,
            bg=bg_color
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Create listbox with scrollbar
        list_frame = tk.Frame(parent, bg=bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        entries_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 9),
            bg=button_color,
            fg="#ffffff",
            yscrollcommand=scrollbar.set
        )
        entries_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=entries_listbox.yview)
        
        # Add entries to listbox
        for entry in entries[:100]:  # Show last 100 entries
            timestamp = datetime.fromisoformat(entry.timestamp).strftime("%d/%m/%Y %H:%M")
            sign = "+" if entry.entry_type == "income" else "-"
            entry_text = f"{timestamp} | {sign}R$ {entry.amount:.2f} | {entry.payment_method} | {entry.description[:30]}"
            entries_listbox.insert(tk.END, entry_text)
    
    def create_users_tab(self, parent, bg_color, fg_color, button_color):
        """Create users management tab"""
        users = self.data_store.load_users()
        
        # Title
        tk.Label(
            parent,
            text="👥 GERENCIAMENTO DE USUÁRIOS",
            font=("Courier", 12, "bold"),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=10)
        
        # Users list
        list_frame = tk.Frame(parent, bg=bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        users_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 10),
            bg=button_color,
            fg="#ffffff",
            yscrollcommand=scrollbar.set
        )
        users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=users_listbox.yview)
        
        # Add users to listbox
        for user in users:
            role_badge = "[ADMIN]" if user.is_admin() else "[USER]"
            user_text = f"{user.username} {role_badge} | Créditos: R$ {user.credits:.2f}"
            users_listbox.insert(tk.END, user_text)
        
        # Button to add new user
        tk.Button(
            parent,
            text="➕ Adicionar Novo Usuário",
            font=("Courier", 10, "bold"),
            bg=button_color,
            fg=fg_color,
            command=self.add_new_user_dialog,
            width=25,
            relief=tk.RAISED,
            bd=3
        ).pack(pady=10)
    
    def create_transactions_tab(self, parent, bg_color, fg_color, button_color):
        """Create transactions tab"""
        transactions = self.data_store.load_transactions()
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Title
        tk.Label(
            parent,
            text="💳 HISTÓRICO DE TRANSAÇÕES",
            font=("Courier", 12, "bold"),
            fg=fg_color,
            bg=bg_color
        ).pack(pady=10)
        
        # Transactions list
        list_frame = tk.Frame(parent, bg=bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        transactions_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 9),
            bg=button_color,
            fg="#ffffff",
            yscrollcommand=scrollbar.set
        )
        transactions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=transactions_listbox.yview)
        
        # Add transactions to listbox
        for transaction in transactions[:200]:  # Show last 200 transactions
            timestamp = datetime.fromisoformat(transaction.timestamp).strftime("%d/%m/%Y %H:%M")
            trans_text = f"{timestamp} | {transaction.username} | R$ {transaction.amount:.2f} | {transaction.payment_method} | {transaction.description[:25]}"
            transactions_listbox.insert(tk.END, trans_text)
    
    def add_new_user_dialog(self):
        """Dialog to add a new user"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Novo Usuário")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        bg_color = "#2a2a2a"
        fg_color = "#00ff00"
        button_color = "#1a1a1a"
        
        dialog.configure(bg=bg_color)
        
        # Title
        tk.Label(
            dialog,
            text="➕ NOVO USUÁRIO",
            font=("Courier", 14, "bold"),
            fg="#ff6600",
            bg=bg_color
        ).pack(pady=15)
        
        # Username
        tk.Label(dialog, text="Username:", font=("Courier", 10), fg=fg_color, bg=bg_color).pack(pady=(10, 0))
        username_entry = tk.Entry(dialog, font=("Courier", 12), bg=button_color, fg="#ffffff")
        username_entry.pack(pady=5)
        
        # Password
        tk.Label(dialog, text="Password:", font=("Courier", 10), fg=fg_color, bg=bg_color).pack(pady=(10, 0))
        password_entry = tk.Entry(dialog, font=("Courier", 12), bg=button_color, fg="#ffffff", show="*")
        password_entry.pack(pady=5)
        
        # Role
        tk.Label(dialog, text="Role:", font=("Courier", 10), fg=fg_color, bg=bg_color).pack(pady=(10, 0))
        role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(dialog, bg=bg_color)
        role_frame.pack(pady=5)
        tk.Radiobutton(role_frame, text="User", variable=role_var, value="user", 
                       bg=bg_color, fg=fg_color, selectcolor=button_color).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(role_frame, text="Admin", variable=role_var, value="admin",
                       bg=bg_color, fg=fg_color, selectcolor=button_color).pack(side=tk.LEFT, padx=10)
        
        # Initial credits
        tk.Label(dialog, text="Créditos Iniciais:", font=("Courier", 10), fg=fg_color, bg=bg_color).pack(pady=(10, 0))
        credits_entry = tk.Entry(dialog, font=("Courier", 12), bg=button_color, fg="#ffffff")
        credits_entry.insert(0, "0.0")
        credits_entry.pack(pady=5)
        
        def create_user():
            username = username_entry.get().strip()
            password = password_entry.get()
            role = role_var.get()
            
            try:
                credits = float(credits_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Créditos inválidos", parent=dialog)
                return
            
            if not username or not password:
                messagebox.showerror("Erro", "Username e password são obrigatórios", parent=dialog)
                return
            
            # Check if user already exists
            if self.data_store.get_user(username):
                messagebox.showerror("Erro", "Usuário já existe", parent=dialog)
                return
            
            # Create new user
            new_user = User(
                username=username,
                password_hash=self.data_store._hash_password(password),
                role=role,
                credits=credits
            )
            self.data_store.update_user(new_user)
            
            messagebox.showinfo("Sucesso", f"Usuário '{username}' criado com sucesso!", parent=dialog)
            dialog.destroy()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=bg_color)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Criar", command=create_user, font=("Courier", 10, "bold"),
                  bg=button_color, fg=fg_color, width=10, relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancelar", command=dialog.destroy, font=("Courier", 10, "bold"),
                  bg="#cc0000", fg="#ffffff", width=10, relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=5)


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
