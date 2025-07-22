"""
Sidebar Components for TalentScout Hiring Assistant
Contains sidebar layout and functionality
"""

import streamlit as st
from .ui_components import display_system_status, display_stats, display_help_section


def display_sidebar_header():
    """Display the sidebar header"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem; 
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                border-radius: 12px; border: 1px solid #0ea5e9;">
        <h1 style="margin: 0; color: #0c4a6e !important; font-size: 1.5rem;">🎛️ Interview Control</h1>
    </div>
    """, unsafe_allow_html=True)


def display_instructions():
    """Display how-to instructions"""
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                border: 1px solid #e5e7eb; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <h3 style="color: #374151 !important; font-size: 1.1rem; margin-bottom: 1rem; 
                   border-bottom: 2px solid #f3f4f6; padding-bottom: 0.5rem;">
            📝 How it works:
        </h3>
        <div style="color: #6b7280; line-height: 1.6;">
            <div style="margin-bottom: 0.75rem; display: flex; align-items: center;">
                <span style="background: #2563eb; color: white; border-radius: 50%; 
                             width: 24px; height: 24px; display: inline-flex; align-items: center; 
                             justify-content: center; margin-right: 0.75rem; font-size: 0.8rem; font-weight: bold;">1</span>
                Click "START MY INTERVIEW" below
            </div>
            <div style="margin-bottom: 0.75rem; display: flex; align-items: center;">
                <span style="background: #2563eb; color: white; border-radius: 50%; 
                             width: 24px; height: 24px; display: inline-flex; align-items: center; 
                             justify-content: center; margin-right: 0.75rem; font-size: 0.8rem; font-weight: bold;">2</span>
                Chat naturally with the AI interviewer
            </div>
            <div style="display: flex; align-items: center;">
                <span style="background: #2563eb; color: white; border-radius: 50%; 
                             width: 24px; height: 24px; display: inline-flex; align-items: center; 
                             justify-content: center; margin-right: 0.75rem; font-size: 0.8rem; font-weight: bold;">3</span>
                Complete your screening journey
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_control_buttons():
    """Display the main control buttons"""
    st.markdown("### Quick Actions")
    
    if st.button("Start New Interview", type="primary", use_container_width=True):
        st.session_state.chatbot.reset_conversation()
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()
    
    st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
    
    if st.button("Reset Current Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()


def display_sidebar():
    """Display the complete sidebar"""
    with st.sidebar:
        # Header
        display_sidebar_header()
        
        # Instructions
        display_instructions()
        
        st.markdown("---")
        
        # Control buttons
        display_control_buttons()
        
        st.markdown("---")
        
        # System status
        st.markdown("### System Status")
        display_system_status()
        
        # Statistics
        try:
            candidates = st.session_state.data_handler.get_all_candidates()
            candidates_count = len(candidates) if candidates else 0
            display_stats(candidates_count)
        except:
            display_stats(0)
        
        # Help section
        st.markdown("---")
        st.markdown("### 💡 Need Help?")
        display_help_section()
