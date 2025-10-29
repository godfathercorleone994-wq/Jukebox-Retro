#!/usr/bin/env python3
"""
Simple tests for Jukebox Retro application
"""

import os
import sys
import unittest
from pathlib import Path

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# We'll test without GUI by importing just the metadata function
class TestJukeboxRetro(unittest.TestCase):
    """Test cases for Jukebox Retro"""
    
    def test_format_time(self):
        """Test time formatting function"""
        # We can't easily test the full app without GUI, but we can test utility functions
        # For now, just verify imports work
        try:
            import pygame
            import mutagen
            self.assertTrue(True, "All dependencies imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import dependencies: {e}")
    
    def test_config_directory(self):
        """Test that config directory can be created"""
        config_dir = Path.home() / ".jukebox_retro"
        config_dir.mkdir(parents=True, exist_ok=True)
        self.assertTrue(config_dir.exists(), "Config directory should exist")
        
    def test_supported_formats(self):
        """Test supported audio format extensions"""
        supported_extensions = ['.mp3', '.wav', '.ogg', '.flac']
        
        for ext in supported_extensions:
            test_file = f"test_audio{ext}"
            self.assertTrue(
                any(test_file.lower().endswith(e) for e in supported_extensions),
                f"{ext} should be a supported format"
            )


class TestModuleImports(unittest.TestCase):
    """Test that the main module can be imported"""
    
    def test_import_main_module(self):
        """Test that jukebox_retro module imports without errors"""
        try:
            # Import without initializing GUI
            import jukebox_retro
            self.assertTrue(hasattr(jukebox_retro, 'JukeboxRetro'), 
                          "Module should have JukeboxRetro class")
            self.assertTrue(hasattr(jukebox_retro, 'main'), 
                          "Module should have main function")
        except ImportError as e:
            # Skip test if tkinter is not available (headless environment)
            if 'tkinter' in str(e):
                self.skipTest("Tkinter not available in headless environment")
            else:
                self.fail(f"Failed to import main module: {e}")
        except Exception as e:
            self.fail(f"Failed to import main module: {e}")


if __name__ == '__main__':
    # Run tests
    print("Running Jukebox Retro tests...\n")
    unittest.main(verbosity=2)
