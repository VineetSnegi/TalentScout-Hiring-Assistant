"""
TalentScout Hiring Assistant - Main Application
===============================================

A comprehensive AI-powered hiring assistant built with Streamlit.
Provides intelligent candidate screening through natural conversation.

Features:
- AI-powered interview conversation using Google Gemini
- Progressive interview stages with dynamic questioning
- Modern, responsive UI with animations
- Comprehensive candidate data collection and storage

Author: Your Name
Date: July 2025
"""

import streamlit as st
from typing import List, Tuple

# Core application imports
from src.core.chatbot import HiringAssistantChatbot
from src.core.data_handler import DataHandler
from src.core.config import APP_TITLE, APP_ICON, COMPANY_NAME

# UI component imports
from src.ui.styles import get_main_css
from src.ui.ui_components import (
    display_header, display_welcome_card, display_completion_message,
    display_chat_message, display_input_section, display_footer
)
from src.ui.enhanced_components import (
    create_animated_progress_bar, create_tech_stack_selector, add_page_transitions
)
from src.ui.sidebar import display_sidebar
from src.ui.progress import display_candidate_progress

# Configure Streamlit page settings
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS styling
st.markdown(get_main_css(), unsafe_allow_html=True)

# Add page transition animations
add_page_transitions()


def initialize_session_state():
    """
    Initialize Streamlit session state variables for the application.
    
    Sets up:
    - Chatbot instance with error handling
    - Message history storage
    - Conversation state tracking
    - Data handler for candidate information
    - Input counter for unique form keys
    """
    # Initialize AI chatbot with error handling
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = HiringAssistantChatbot()
            st.session_state.chat_initialized = True
        except Exception as e:
            st.session_state.chat_initialized = False
            st.session_state.initialization_error = str(e)
    
    # Initialize conversation storage
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Track conversation state
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    # Initialize data handler for candidate information
    if 'data_handler' not in st.session_state:
        st.session_state.data_handler = DataHandler()
    
    # Counter for unique form keys (prevents Streamlit form conflicts)
    if 'input_counter' not in st.session_state:
        st.session_state.input_counter = 0


def check_user_exit_intent(messages: List[Tuple[str, str]]) -> bool:
    """
    Analyze user messages to detect if they want to end the conversation.
    
    Args:
        messages: List of (role, message) tuples from the conversation
        
    Returns:
        bool: True if user expressed intent to exit, False otherwise
    """
    if not messages:
        return False
    
    # Extract only user messages and check the most recent one
    last_user_messages = [msg[1].lower() for msg in messages if msg[0] == "user"]
    if last_user_messages:
        last_message = last_user_messages[-1]
        exit_keywords = ["bye", "goodbye", "exit", "quit", "end conversation", "stop interview"]
        return any(keyword in last_message for keyword in exit_keywords)
    return False


def handle_user_input(user_input: str):
    """
    Process user input and generate AI response.
    
    This function:
    1. Adds user message to conversation history
    2. Generates AI response using the chatbot
    3. Handles errors gracefully with fallback responses
    4. Increments input counter for form management
    
    Args:
        user_input: The user's message text
    """
    if user_input.strip():
        # Add user message
        st.session_state.messages.append(("user", user_input))
        
        # Increment counter to create new input widget (clears the text)
        st.session_state.input_counter += 1
        
        # Get bot response with enhanced loading
        try:
            with st.spinner("🤔 AI is thinking... Please wait a moment."):
                bot_response = st.session_state.chatbot.process_message(user_input)
                st.session_state.messages.append(("assistant", bot_response))
            st.rerun()
        except Exception as e:
            st.error(f"❌ **Error occurred:** {e}")
            st.info("💡 **Tip:** Try refreshing the page or restarting the interview.")


def display_chat_interface():
    """
    Display the main chat interface for the hiring assistant.
    
    This function handles:
    - Welcome screen with start button
    - Chat message history display
    - User input form with send button
    - Conversation completion detection
    - Progress tracking throughout the interview
    """
    # Verify chatbot initialization
    if not st.session_state.get('chat_initialized', False):
        st.error("❌ **Chatbot initialization failed** - Please check your Google AI API key in the .env file")
        return
    
    # Display welcome screen for new users
    if not st.session_state.conversation_started:
        display_welcome_card()
        
        # Start interview button
        if st.button("START MY INTERVIEW", type="primary", use_container_width=True):
            # Initialize conversation with AI greeting
            initial_response = st.session_state.chatbot.process_message("hello")
            st.session_state.messages.append(("assistant", initial_response))
            st.session_state.conversation_started = True
            st.rerun()
        return

    # Main interview interface
    st.markdown("## 💬 Interview Chat")
    
    # Create container for all chat content
    chat_container = st.container()
    
    with chat_container:
        for role, message in st.session_state.messages:
            display_chat_message(role, message)
    
    # Get chatbot instance for later use
    chatbot = st.session_state.chatbot
    
    # Check conversation status
    conversation_completed = (chatbot.conversation_stage == "completion")
    user_wants_exit = check_user_exit_intent(st.session_state.messages)
    
    # Input section - right after chat messages in the same container
    if not (conversation_completed or user_wants_exit):
        with chat_container:
            st.markdown("""
            <div style="margin: 1rem 0; padding: 1rem; background: #f8fafc; border-radius: 8px; border-left: 4px solid #3b82f6;">
                <p style="margin: 0; color: #1f2937; font-size: 0.9rem;">
                    💬 <strong>Your turn to respond:</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create input form with proper layout
            with st.form(key=f"response_form_{st.session_state.input_counter}", clear_on_submit=True):
                # Create columns for input and button - button on the right
                col_input, col_button = st.columns([5, 1])
                
                with col_input:
                    user_input = st.text_input(
                        "Your Response:",
                        placeholder="Type your response here and press Enter to send...",
                        key=f"response_input_{st.session_state.input_counter}",
                        label_visibility="collapsed"
                    )
                
                with col_button:
                    send_clicked = st.form_submit_button(
                        "Send",
                        use_container_width=True,
                        type="primary"
                    )
            
            if send_clicked and user_input and user_input.strip():
                handle_user_input(user_input.strip())
                st.rerun()
    else:
        # Show completion message
        display_completion_message(conversation_completed)
    
    # Separator before progress sections
    st.markdown("---")
    
    # Show progress
    if st.session_state.conversation_started and not (conversation_completed or user_wants_exit):
        display_candidate_progress()


def main():
    """Main application entry point"""
    # Initialize
    initialize_session_state()
    
    # Display components
    display_header()
    display_chat_interface()
    display_sidebar()
    
    # Footer
    st.markdown("---")
    display_footer()


if __name__ == "__main__":
    main()
