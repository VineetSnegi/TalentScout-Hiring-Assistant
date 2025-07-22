# TalentScout Hiring Assistant Launcher (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TalentScout Hiring Assistant Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "📥 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Failed to install requirements" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Requirements installed" -ForegroundColor Green

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  WARNING: .env file not found" -ForegroundColor Yellow
    Write-Host "📄 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "🔑 IMPORTANT: Please edit .env file and add your Google AI API key" -ForegroundColor Magenta
    Write-Host "🌐 Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host ""
    
    $response = Read-Host "Do you want to open the .env file now? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        notepad .env
    }
}

# Start the application
Write-Host ""
Write-Host "🚀 Starting TalentScout Hiring Assistant..." -ForegroundColor Green
Write-Host "🌐 The application will open in your default web browser" -ForegroundColor Cyan
Write-Host "🔗 URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host "⏹️  Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

try {
    streamlit run app.py
} catch {
    Write-Host "❌ Error starting application: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "👋 Application stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"

