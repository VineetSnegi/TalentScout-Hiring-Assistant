"""
Test script for TalentScout Hiring Assistant
Verify that all components are working correctly
"""

import os
import sys
from pathlib import Path
import json


def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google AI imported successfully")
    except ImportError as e:
        print(f"❌ Google AI import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True


def test_custom_modules():
    """Test if custom modules can be imported"""
    print("\n🧪 Testing custom modules...")
    
    try:
        from config import APP_TITLE, TECH_CATEGORIES
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from data_handler import DataHandler
        print("✅ DataHandler imported successfully")
    except ImportError as e:
        print(f"❌ DataHandler import failed: {e}")
        return False
    
    try:
        from chatbot import HiringAssistantChatbot
        print("✅ Chatbot module imported successfully")
    except ImportError as e:
        print(f"❌ Chatbot import failed: {e}")
        return False
    
    return True


def test_environment():
    """Test environment configuration"""
    print("\n🧪 Testing environment...")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        if api_key == "your_google_ai_api_key_here":
            print("⚠️  Google AI API key placeholder found - please update with real key")
        else:
            print("✅ Google AI API key configured")
    else:
        print("❌ Google AI API key not found")
        return False
    
    return True


def test_data_handler():
    """Test data handler functionality"""
    print("\n🧪 Testing data handler...")
    
    try:
        from data_handler import DataHandler
        handler = DataHandler()
        print("✅ DataHandler instantiated successfully")
        
        # Test data validation
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "123-456-7890",
            "experience_years": 3,
            "desired_position": "Software Engineer"
        }
        
        is_valid, errors = handler.validate_candidate_data(test_data)
        if is_valid:
            print("✅ Data validation working")
        else:
            print(f"❌ Data validation failed: {errors}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ DataHandler test failed: {e}")
        return False


def test_chatbot_initialization():
    """Test chatbot initialization (requires API key)"""
    print("\n🧪 Testing chatbot initialization...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_ai_api_key_here":
        print("⚠️  Skipping chatbot test - API key not configured")
        return True
    
    try:
        from chatbot import HiringAssistantChatbot
        chatbot = HiringAssistantChatbot()
        print("✅ Chatbot initialized successfully")
        
        # Test basic functionality
        response = chatbot.process_message("hello")
        if response and len(response) > 10:
            print("✅ Chatbot responding correctly")
            return True
        else:
            print("❌ Chatbot not responding properly")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")
        return False


def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        "app.py",
        "chatbot.py", 
        "data_handler.py",
        "config.py",
        "requirements.txt",
        "README.md",
        ".env",
        ".gitignore"
    ]
    
    all_present = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            all_present = False
    
    return all_present


def run_all_tests():
    """Run all tests"""
    print("🎯 TalentScout Hiring Assistant - Component Tests")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("Custom Modules", test_custom_modules),
        ("Environment", test_environment),
        ("Data Handler", test_data_handler),
        ("Chatbot Initialization", test_chatbot_initialization)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Your application is ready to run.")
        print("\n🚀 To start the application:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   - Install requirements: pip install -r requirements.txt")
        print("   - Set up API key in .env file")
        print("   - Check file permissions")

if __name__ == "__main__":
    run_all_tests()
