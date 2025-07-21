#!/bin/bash

# TalentScout Hiring Assistant - Cloud Deployment Script
# This script helps deploy the application to various cloud platforms

echo "🚀 TalentScout Hiring Assistant - Cloud Deployment Helper"
echo "========================================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your GOOGLE_API_KEY"
    echo "Example: echo 'GOOGLE_API_KEY=your_key_here' > .env"
    exit 1
fi

echo "📋 Available deployment options:"
echo "1. Streamlit Cloud (Recommended)"
echo "2. Heroku"
echo "3. Google Cloud Run"
echo "4. AWS EC2"
echo "5. Local Docker"
echo ""

read -p "Select deployment option (1-5): " choice

case $choice in
    1)
        echo "🌟 Streamlit Cloud Deployment Instructions:"
        echo "----------------------------------------"
        echo "1. Push your code to GitHub (make sure .env is in .gitignore)"
        echo "2. Go to https://share.streamlit.io/"
        echo "3. Connect your GitHub repository"
        echo "4. Set GOOGLE_API_KEY in Streamlit Cloud secrets"
        echo "5. Deploy with these settings:"
        echo "   - Main file: app.py"
        echo "   - Python version: 3.8+"
        echo ""
        echo "📝 Don't forget to add your secrets in Streamlit Cloud:"
        echo "   GOOGLE_API_KEY = \"your_gemini_api_key_here\""
        ;;
    2)
        echo "🟪 Heroku Deployment Instructions:"
        echo "--------------------------------"
        echo "1. Install Heroku CLI"
        echo "2. Login: heroku login"
        echo "3. Create app: heroku create talentscout-hiring-assistant"
        echo "4. Set environment variables:"
        echo "   heroku config:set GOOGLE_API_KEY=your_key_here"
        echo "5. Deploy: git push heroku main"
        echo ""
        # Create Procfile for Heroku
        echo "web: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile
        echo "✅ Created Procfile for Heroku"
        ;;
    3)
        echo "☁️ Google Cloud Run Deployment:"
        echo "-----------------------------"
        echo "1. Enable Cloud Run API in Google Cloud Console"
        echo "2. Build and deploy:"
        echo "   gcloud run deploy talentscout --source ."
        echo "3. Set environment variables in Cloud Run console"
        echo ""
        # Create Dockerfile for Cloud Run
        cat > Dockerfile << 'EOF'
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
EOF
        echo "✅ Created Dockerfile for Google Cloud Run"
        ;;
    4)
        echo "🟠 AWS EC2 Deployment Instructions:"
        echo "---------------------------------"
        echo "1. Launch an EC2 instance (Ubuntu 20.04+)"
        echo "2. SSH into your instance"
        echo "3. Install Python and pip:"
        echo "   sudo apt update && sudo apt install python3 python3-pip"
        echo "4. Clone your repository and install dependencies"
        echo "5. Set up environment variables"
        echo "6. Run with: nohup streamlit run app.py --server.port 8501 &"
        echo "7. Configure security group to allow port 8501"
        ;;
    5)
        echo "🐳 Local Docker Deployment:"
        echo "-------------------------"
        # Create Dockerfile for local deployment
        cat > Dockerfile << 'EOF'
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
EOF

        # Create docker-compose.yml
        cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  talentscout:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./data:/app/data
EOF

        echo "✅ Created Dockerfile and docker-compose.yml"
        echo ""
        echo "To run with Docker:"
        echo "1. Build: docker build -t talentscout ."
        echo "2. Run: docker run -p 8501:8501 --env-file .env talentscout"
        echo ""
        echo "Or with Docker Compose:"
        echo "docker-compose up -d"
        ;;
    *)
        echo "❌ Invalid option selected"
        exit 1
        ;;
esac

echo ""
echo "📚 Additional Resources:"
echo "----------------------"
echo "- Streamlit Deployment Guide: https://docs.streamlit.io/streamlit-community-cloud"
echo "- Heroku Python Guide: https://devcenter.heroku.com/articles/getting-started-with-python"
echo "- Google Cloud Run: https://cloud.google.com/run/docs/quickstarts/build-and-deploy"
echo ""
echo "🔐 Security Reminders:"
echo "- Never commit .env files to version control"
echo "- Use environment variables for API keys"
echo "- Enable HTTPS in production"
echo "- Consider implementing rate limiting"
echo ""
echo "✅ Deployment helper completed!"
