"""
Setup script for TalentScout Hiring Assistant
Run this script to set up the project environment
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def setup_env_file():
    """Set up environment file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from example")
        print("⚠️  Please add your Google AI API key to the .env file")
        return True
    else:
        print("❌ .env.example file not found")
        return False


def create_data_directory():
    """Create data directory for storing candidate information"""
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
        print("✅ Data directory created")
    else:
        print("✅ Data directory already exists")


def run_application():
    """Ask user if they want to run the application"""
    response = input("\n🚀 Would you like to start the application now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        print("\n🎯 Starting TalentScout Hiring Assistant...")
        print("📱 The application will open in your default web browser")
        print("🔗 URL: http://localhost:8501")
        print("\n💡 To stop the application, press Ctrl+C in this terminal")
        
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
        except Exception as e:
            print(f"\n❌ Error running application: {e}")
    else:
        print("\n📋 Setup complete! To run the application later, use:")
        print("   streamlit run app.py")


def main():
    """Main setup function"""
    print("🎯 TalentScout Hiring Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup environment file
    if not setup_env_file():
        return
    
    # Create data directory
    create_data_directory()
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your Google AI API key to the .env file")
    print("   - Get your key from: https://makersuite.google.com/app/apikey")
    print("   - Edit .env file and replace 'your_google_ai_api_key_here' with your actual key")
    print("2. Run the application with: streamlit run app.py")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key and api_key != "your_google_ai_api_key_here":
        print("\n✅ Google AI API key is configured")
        run_application()
    else:
        print("\n⚠️  Please set up your Google AI API key before running the application")


if __name__ == "__main__":
    main()
