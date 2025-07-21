"""
Quick test script to verify the reorganized structure works
"""

try:
    print("🔄 Testing imports...")
    
    # Test core imports
    from src.core.chatbot import HiringAssistantChatbot
    from src.core.data_handler import DataHandler
    from src.core.config import APP_TITLE, APP_ICON, COMPANY_NAME
    print("✅ Core imports successful")
    
    # Test UI imports
    from src.ui.styles import get_main_css
    from src.ui.ui_components import display_header
    from src.ui.sidebar import display_sidebar
    from src.ui.progress import display_candidate_progress
    print("✅ UI imports successful")
    
    print("🎉 All imports working correctly!")
    print(f"📋 App Title: {APP_TITLE}")
    print("🏗️ Project structure is clean and organized!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
