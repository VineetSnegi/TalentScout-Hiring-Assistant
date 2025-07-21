"""
Progress Components for TalentScout Hiring Assistant
Contains progress tracking and display functionality
"""

import streamlit as st
from .enhanced_components import create_animated_progress_bar


def display_basic_info_progress(completed: int, total: int):
    """Display progress for basic information collection"""
    progress_percent = completed / total if total > 0 else 0
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, white 0%, #f8fafc 100%); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid #e5e7eb; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin: 1.5rem 0;">
        <h3 style="color: #1f2937; margin-bottom: 1rem; display: flex; align-items: center;">
            <span style="margin-left: 0.5rem;">Basic Information Collection</span>
        </h3>
        <div style="margin: 1rem 0;">
            <div style="background: #f3f4f6; border-radius: 8px; height: 12px; border: 2px solid #e5e7eb; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #10b981 0%, #059669 100%); 
                            height: 100%; width: {progress_percent * 100}%; border-radius: 6px; transition: width 0.3s ease;"></div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    margin-top: 1rem; padding: 0.75rem; background: #f1f5f9; border-radius: 8px;">
            <span style="color: #475569; font-weight: 500;">Progress Details:</span>
            <span style="color: #059669; font-weight: 600;">{completed} of {total} fields completed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_tech_stack_progress():
    """Display progress for tech stack discussion"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, white 0%, #f0f9ff 100%); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid #0ea5e9; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin: 1.5rem 0;">
        <h3 style="color: #0c4a6e; margin-bottom: 1rem; display: flex; align-items: center;">
            💻 <span style="margin-left: 0.5rem;">Technical Background Discussion</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(0.7)  # 70% complete
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                margin: 0.5rem 0; padding: 0.75rem; background: #e0f2fe; border-radius: 8px;">
        <span style="color: #0e7490; font-weight: 500;">Current Stage:</span>
        <span style="color: #0c4a6e; font-weight: 600;">Discussing your tech skills and experience</span>
    </div>
    """, unsafe_allow_html=True)


def display_technical_questions_progress():
    """Display progress for technical questions"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, white 0%, #fef3c7 100%); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid #d97706; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin: 1.5rem 0;">
        <h3 style="color: #92400e; margin-bottom: 1rem; display: flex; align-items: center;">
            🔬 <span style="margin-left: 0.5rem;">Technical Assessment</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(0.9)  # 90% complete
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                margin: 0.5rem 0; padding: 0.75rem; background: #fef3c7; border-radius: 8px;">
        <span style="color: #a16207; font-weight: 500;">Current Stage:</span>
        <span style="color: #92400e; font-weight: 600;">Technical interview in progress...</span>
    </div>
    """, unsafe_allow_html=True)


def display_completion_progress():
    """Display progress for completed interview"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, white 0%, #d1fae5 100%); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid #059669; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin: 1.5rem 0;">
        <h3 style="color: #065f46; margin-bottom: 1rem; display: flex; align-items: center;">
            🎉 <span style="margin-left: 0.5rem;">Interview Completed!</span>
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(1.0)  # 100% complete
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                margin: 0.5rem 0; padding: 0.75rem; background: #d1fae5; border-radius: 8px;">
        <span style="color: #047857; font-weight: 500;">Status:</span>
        <span style="color: #065f46; font-weight: 600;">✅ All stages completed successfully!</span>
    </div>
    """, unsafe_allow_html=True)


def display_candidate_progress():
    """Display enhanced progress tracker based on conversation stage"""
    if not st.session_state.conversation_started:
        return
    
    try:
        chatbot = st.session_state.chatbot
        candidate_info = chatbot.get_candidate_info()
        
        # Determine current step and progress
        current_step = 1
        progress = 0.0
        
        if chatbot.conversation_stage == "greeting":
            return  # No progress bar during greeting
        
        elif chatbot.conversation_stage == "collecting_info":
            current_step = 2
            # Check how many basic info fields are complete
            basic_fields = ['name', 'email', 'phone', 'experience_years', 'desired_position', 'location']
            completed = sum(1 for field in basic_fields if candidate_info.get(field))
            total = len(basic_fields)
            progress = (completed / total) * 0.4  # 40% of total progress
            
        elif chatbot.conversation_stage == "tech_stack":
            current_step = 3
            progress = 0.6  # 60% complete
            
        elif chatbot.conversation_stage == "technical_questions":
            current_step = 4
            progress = 0.8  # 80% complete
            
        elif chatbot.conversation_stage == "completion":
            current_step = 5
            progress = 1.0  # 100% complete
        
        # Display the enhanced animated progress bar (single column)
        st.markdown("### Interview Progress")
        create_animated_progress_bar(progress, 5, current_step)
        
        # Show additional details based on stage (without Basic Information Collection)
        if chatbot.conversation_stage == "tech_stack":
            display_tech_stack_progress()
            
        elif chatbot.conversation_stage == "technical_questions":
            display_technical_questions_progress()
            
        elif chatbot.conversation_stage == "completion":
            display_completion_progress()
        
    except Exception as e:
        pass  # Simplified - no error display
