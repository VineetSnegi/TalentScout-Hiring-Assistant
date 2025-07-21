"""
UI Components for TalentScout Hiring Assistant
Contains reusable UI components and layouts
"""

import streamlit as st
import os
from typing import Optional


def display_header():
    """Display the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>TalentScout Hiring Assistant</h1>
        <p>AI-powered candidate screening made simple</p>
    </div>
    """, unsafe_allow_html=True)


def display_welcome_card():
    """Display the welcome card for new users"""
    st.markdown("""
    <div class="info-card">
        <h2>🎯 Ready for your AI interview?</h2>
        <p style="font-size: 1.1rem; margin: 1rem 0; color: #4b5563;">
            I'm your AI interviewer and I'll guide you through a friendly conversation about your background and technical skills.
        </p>
        <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    padding: 1rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #d97706;">
            <strong style="color: #92400e;">⏱️ Duration:</strong> <span style="color: #92400e;">About 10-15 minutes</span><br>
            <strong style="color: #92400e;">📋 What we'll cover:</strong> <span style="color: #92400e;">Personal info, experience, and tech skills</span>
        </div>
        <p style="color: #6b7280; font-size: 0.95rem; margin-top: 1.5rem;">
            💡 <em>Tip: Answer naturally and take your time. This is a friendly conversation, not a test!</em>
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_completion_message(conversation_completed: bool):
    """Display completion or exit message"""
    if conversation_completed:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #bbf7d0 100%); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #059669; 
                    text-align: center; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #065f46; margin-bottom: 1rem;">🎉 Interview Completed Successfully!</h3>
            <p style="color: #047857; font-size: 1.1rem; margin-bottom: 1rem;">
                Thank you for taking the time to complete your interview. Your responses have been recorded.
            </p>
            <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="color: #065f46; margin: 0; font-weight: 500;">
                    💡 What's next? Our team will review your responses and get back to you soon!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #2563eb; 
                    text-align: center; margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #1e40af; margin-bottom: 1rem;">👋 Interview Ended</h3>
            <p style="color: #3730a3; font-size: 1.1rem; margin-bottom: 1rem;">
                You chose to end the interview early. No problem at all!
            </p>
            <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="color: #1e40af; margin: 0; font-weight: 500;">
                    💡 Feel free to start a new interview anytime using the sidebar controls.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_chat_message(role: str, message: str):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
        <strong>You:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
        <strong>🤖 Interviewer:</strong><br>{message}
        </div>
        """, unsafe_allow_html=True)


def display_input_section():
    """Display the input section for active conversations with embedded chat input"""
    # Clean chat input without extra styling wrapper
    user_input = st.chat_input(
        placeholder="Type your response here and press Enter to continue the conversation...",
        key=f"chat_input_{st.session_state.input_counter}"
    )
    
    return user_input


def display_system_status():
    """Display system status information"""
    api_status = os.getenv("GOOGLE_API_KEY")
    if api_status:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #bbf7d0 100%); 
                    padding: 0.75rem; border-radius: 8px; border-left: 4px solid #059669; margin-bottom: 1rem;">
            <strong style="color: #065f46;">✅ AI System Connected</strong><br>
            <span style="color: #047857; font-size: 0.9rem;">Ready for interviews</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                    padding: 0.75rem; border-radius: 8px; border-left: 4px solid #dc2626; margin-bottom: 1rem;">
            <strong style="color: #991b1b;">❌ AI System Error</strong><br>
            <span style="color: #b91c1c; font-size: 0.9rem;">Check API configuration</span>
        </div>
        """, unsafe_allow_html=True)


def display_stats(candidates_count: int):
    """Display interview statistics"""
    if candidates_count > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid #2563eb;">
            <div style="font-size: 2rem; font-weight: bold; color: #1e40af; margin-bottom: 0.25rem;">{candidates_count}</div>
            <div style="color: #3730a3; font-size: 0.9rem; font-weight: 500;">Total Interviews Completed</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                    padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid #9ca3af;">
            <div style="font-size: 2rem; font-weight: bold; color: #6b7280; margin-bottom: 0.25rem;">0</div>
            <div style="color: #6b7280; font-size: 0.9rem; font-weight: 500;">No interviews yet</div>
        </div>
        """, unsafe_allow_html=True)


def display_help_section():
    """Display help information"""
    st.markdown("""
    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="color: #475569; font-size: 0.9rem; line-height: 1.5;">
            <strong>Having issues?</strong><br>
            • Try refreshing the page<br>
            • Check your internet connection<br>
            • Use "Reset" to start over<br>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_footer():
    """Display the application footer"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                border-radius: 12px; margin-top: 2rem; border: 1px solid #e5e7eb;">
        <div style="color: #64748b; font-size: 0.9rem; line-height: 1.6;">
            <strong style="color: #475569;">🤖 TalentScout</strong> - Intelligent Hiring Assistant<br>
            <span style="color: #94a3b8;">Powered by Google AI • Built with Streamlit • Designed for Modern Recruitment</span>
        </div>
        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(255,255,255,0.7); 
                    border-radius: 8px; color: #6b7280; font-size: 0.85rem;">
            💡 <em>Making hiring conversations more human, one chat at a time.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
