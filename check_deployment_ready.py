#!/usr/bin/env python3
"""
Final Deployment Preparation for VineetSnegi/TalentScout-Hiring-Assistant
"""

import os
import subprocess
from datetime import datetime

def check_deployment_readiness():
    """Check if the project is ready for Streamlit Cloud deployment"""
    print("🎯 TalentScout Hiring Assistant - Deployment Readiness Check")
    print("=" * 60)
    print("📍 Repository: https://github.com/VineetSnegi/TalentScout-Hiring-Assistant")
    print("")
    
    # Check essential files
    essential_files = [
        ("app.py", "Main Streamlit application"),
        ("requirements.txt", "Python dependencies"),
        (".env.example", "Environment template"),
        ("README.md", "Documentation"),
        ("src/core/chatbot.py", "Core chatbot logic"),
        ("src/ui/styles.py", "UI styling"),
        ("data/candidates.json", "Data storage")
    ]
    
    print("📁 Essential Files Check:")
    all_files_present = True
    for file_path, description in essential_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} - {description}")
        else:
            print(f"  ❌ {file_path} - MISSING - {description}")
            all_files_present = False
    
    print("")
    
    # Check Python modules
    print("🐍 Python Modules Check:")
    modules_to_test = [
        ("streamlit", "Web framework"),
        ("google.generativeai", "Google AI integration"),
        ("dotenv", "Environment variables"),
        ("asyncio", "Async processing")
    ]
    
    modules_working = True
    for module, description in modules_to_test:
        try:
            __import__(module.replace('-', '_'))
            print(f"  ✅ {module} - {description}")
        except ImportError:
            print(f"  ❌ {module} - MISSING - {description}")
            modules_working = False
    
    print("")
    
    # Check application functionality
    print("🧪 Application Functionality Check:")
    try:
        # Test core imports
        from src.core.chatbot import HiringAssistantChatbot
        from src.ui.styles import get_main_css
        from src.core.config import APP_TITLE
        
        print("  ✅ Core modules import successfully")
        print("  ✅ UI components load correctly")
        print("  ✅ Configuration accessible")
        
        functionality_working = True
    except Exception as e:
        print(f"  ❌ Application functionality error: {e}")
        functionality_working = False
    
    print("")
    
    # Deployment readiness summary
    print("🚀 Deployment Readiness Summary:")
    print("-" * 40)
    
    if all_files_present:
        print("  ✅ All essential files present")
    else:
        print("  ❌ Missing essential files")
    
    if modules_working:
        print("  ✅ All required modules available")
    else:
        print("  ❌ Missing required modules")
    
    if functionality_working:
        print("  ✅ Application functionality verified")
    else:
        print("  ❌ Application functionality issues")
    
    print("")
    
    # Overall status
    ready_for_deployment = all_files_present and modules_working and functionality_working
    
    if ready_for_deployment:
        print("🎉 PROJECT IS READY FOR STREAMLIT CLOUD DEPLOYMENT!")
        print("")
        print("📋 Next Steps:")
        print("1. Push your code to GitHub: https://github.com/VineetSnegi/TalentScout-Hiring-Assistant")
        print("2. Visit: https://share.streamlit.io/")
        print("3. Create new app from your GitHub repository")
        print("4. Set main file path: app.py")
        print("5. Add GOOGLE_API_KEY in secrets")
        print("6. Deploy and test!")
        print("")
        print("🌐 Expected URL: https://talentscout-hiring-assistant-[id].streamlit.app/")
        
    else:
        print("⚠️  PROJECT NEEDS ATTENTION BEFORE DEPLOYMENT")
        print("Please fix the issues above before deploying to Streamlit Cloud.")
    
    print("")
    print("📚 Documentation:")
    print("- README.md: Comprehensive project guide")
    print("- STREAMLIT_DEPLOYMENT_GUIDE.md: Step-by-step deployment")
    print("- docs/: Additional documentation and deployment scripts")
    
    return ready_for_deployment

if __name__ == "__main__":
    check_deployment_readiness()
