#!/bin/bash
# Build script for Jukebox Retro on Linux

echo "==================================="
echo "Jukebox Retro - Build Script"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    exit 1
fi

echo "✅ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Build with PyInstaller
echo "🔨 Building executable with PyInstaller..."
pyinstaller jukebox_retro.spec --clean

if [ $? -ne 0 ]; then
    echo "❌ Error: Build failed"
    exit 1
fi

echo ""
echo "==================================="
echo "✅ Build completed successfully!"
echo "==================================="
echo ""
echo "📁 Executable location: dist/JukeboxRetro"
echo ""
echo "To run the application:"
echo "  ./dist/JukeboxRetro"
echo ""
