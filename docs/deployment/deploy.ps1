# TalentScout Hiring Assistant - Windows Deployment Script
# PowerShell version for Windows users

Write-Host "🚀 TalentScout Hiring Assistant - Cloud Deployment Helper" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your GOOGLE_API_KEY" -ForegroundColor Yellow
    Write-Host "Example: echo 'GOOGLE_API_KEY=your_key_here' > .env" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📋 Available deployment options:" -ForegroundColor Green
Write-Host "1. Streamlit Cloud (Recommended)"
Write-Host "2. Heroku"
Write-Host "3. Google Cloud Run"
Write-Host "4. AWS EC2"
Write-Host "5. Local Docker"
Write-Host ""

$choice = Read-Host "Select deployment option (1-5)"

switch ($choice) {
    1 {
        Write-Host "🌟 Streamlit Cloud Deployment Instructions:" -ForegroundColor Yellow
        Write-Host "----------------------------------------"
        Write-Host "1. Push your code to GitHub (make sure .env is in .gitignore)"
        Write-Host "2. Go to https://share.streamlit.io/"
        Write-Host "3. Connect your GitHub repository"
        Write-Host "4. Set GOOGLE_API_KEY in Streamlit Cloud secrets"
        Write-Host "5. Deploy with these settings:"
        Write-Host "   - Main file: app.py"
        Write-Host "   - Python version: 3.8+"
        Write-Host ""
        Write-Host "📝 Don't forget to add your secrets in Streamlit Cloud:" -ForegroundColor Cyan
        Write-Host '   GOOGLE_API_KEY = "your_gemini_api_key_here"' -ForegroundColor Gray
    }
    
    2 {
        Write-Host "🟪 Heroku Deployment Instructions:" -ForegroundColor Magenta
        Write-Host "--------------------------------"
        Write-Host "1. Install Heroku CLI"
        Write-Host "2. Login: heroku login"
        Write-Host "3. Create app: heroku create talentscout-hiring-assistant"
        Write-Host "4. Set environment variables:"
        Write-Host "   heroku config:set GOOGLE_API_KEY=your_key_here"
        Write-Host "5. Deploy: git push heroku main"
        Write-Host ""
        
        # Create Procfile for Heroku
        "web: streamlit run app.py --server.port `$PORT --server.address 0.0.0.0" | Out-File -FilePath "Procfile" -Encoding utf8
        Write-Host "✅ Created Procfile for Heroku" -ForegroundColor Green
    }
    
    3 {
        Write-Host "☁️ Google Cloud Run Deployment:" -ForegroundColor Blue
        Write-Host "-----------------------------"
        Write-Host "1. Enable Cloud Run API in Google Cloud Console"
        Write-Host "2. Build and deploy:"
        Write-Host "   gcloud run deploy talentscout --source ."
        Write-Host "3. Set environment variables in Cloud Run console"
        Write-Host ""
        
        # Create Dockerfile for Cloud Run
        @"
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
"@ | Out-File -FilePath "Dockerfile" -Encoding utf8
        
        Write-Host "✅ Created Dockerfile for Google Cloud Run" -ForegroundColor Green
    }
    
    4 {
        Write-Host "🟠 AWS EC2 Deployment Instructions:" -ForegroundColor DarkYellow
        Write-Host "---------------------------------"
        Write-Host "1. Launch an EC2 instance (Ubuntu 20.04+)"
        Write-Host "2. SSH into your instance"
        Write-Host "3. Install Python and pip:"
        Write-Host "   sudo apt update && sudo apt install python3 python3-pip"
        Write-Host "4. Clone your repository and install dependencies"
        Write-Host "5. Set up environment variables"
        Write-Host "6. Run with: nohup streamlit run app.py --server.port 8501 &"
        Write-Host "7. Configure security group to allow port 8501"
    }
    
    5 {
        Write-Host "🐳 Local Docker Deployment:" -ForegroundColor Blue
        Write-Host "-------------------------"
        
        # Create Dockerfile for local deployment
        @"
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"@ | Out-File -FilePath "Dockerfile" -Encoding utf8

        # Create docker-compose.yml
        @"
version: '3.8'

services:
  talentscout:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_API_KEY=`${GOOGLE_API_KEY}
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data
"@ | Out-File -FilePath "docker-compose.yml" -Encoding utf8

        Write-Host "✅ Created Dockerfile and docker-compose.yml" -ForegroundColor Green
        Write-Host ""
        Write-Host "To run with Docker:" -ForegroundColor Yellow
        Write-Host "1. Build: docker build -t talentscout ."
        Write-Host "2. Run: docker run -p 8501:8501 --env-file .env talentscout"
        Write-Host ""
        Write-Host "Or with Docker Compose:" -ForegroundColor Yellow
        Write-Host "docker-compose up -d"
    }
    
    default {
        Write-Host "❌ Invalid option selected" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📚 Additional Resources:" -ForegroundColor Cyan
Write-Host "----------------------"
Write-Host "- Streamlit Deployment Guide: https://docs.streamlit.io/streamlit-community-cloud"
Write-Host "- Heroku Python Guide: https://devcenter.heroku.com/articles/getting-started-with-python"
Write-Host "- Google Cloud Run: https://cloud.google.com/run/docs/quickstarts/build-and-deploy"
Write-Host ""
Write-Host "🔐 Security Reminders:" -ForegroundColor Red
Write-Host "- Never commit .env files to version control"
Write-Host "- Use environment variables for API keys"
Write-Host "- Enable HTTPS in production"
Write-Host "- Consider implementing rate limiting"
Write-Host ""
Write-Host "✅ Deployment helper completed!" -ForegroundColor Green
