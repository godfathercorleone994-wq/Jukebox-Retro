@echo off
REM Build script for Jukebox Retro on Windows

echo ===================================
echo Jukebox Retro - Build Script
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed
    exit /b 1
)

echo pip found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo Dependencies installed
echo.

REM Build with PyInstaller
echo Building executable with PyInstaller...
pyinstaller jukebox_retro.spec --clean

if %errorlevel% neq 0 (
    echo Error: Build failed
    exit /b 1
)

echo.
echo ===================================
echo Build completed successfully!
echo ===================================
echo.
echo Executable location: dist\JukeboxRetro.exe
echo.
echo To run the application:
echo   dist\JukeboxRetro.exe
echo.
pause
