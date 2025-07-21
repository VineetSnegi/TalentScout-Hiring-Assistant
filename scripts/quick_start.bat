@echo off
echo 🚀 TalentScout Hiring Assistant - Quick Start
echo =============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Creating .env template...
    echo GOOGLE_API_KEY=your_google_gemini_api_key_here > .env
    echo 📝 Please edit .env file and add your Google Gemini API key
    echo You can get one from: https://makersuite.google.com/app/apikey
    pause
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

echo 🎯 Choose what to run:
echo 1. Main TalentScout Application
echo 2. Feature Demo Showcase
echo 3. Feature Validation Test
echo 4. Exit

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🚀 Starting TalentScout Hiring Assistant...
    python -m streamlit run app.py
) else if "%choice%"=="2" (
    echo 🎪 Starting Feature Demo...
    python -m streamlit run demo.py
) else if "%choice%"=="3" (
    echo 🧪 Running Feature Validation...
    python test_features.py
    pause
) else if "%choice%"=="4" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

pause
