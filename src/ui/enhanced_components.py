"""
Enhanced UI Components for TalentScout Hiring Assistant
Advanced UI elements with animations, voice input, and enhanced UX
"""

import streamlit as st
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import base64

def create_animated_progress_bar(progress: float, total_steps: int, current_step: int) -> None:
    """Create an animated progress bar with step indicators"""
    
    # Custom CSS for animated progress
    progress_css = f"""
    <style>
    .progress-container {{
        background: linear-gradient(90deg, #E5E7EB 0%, #F3F4F6 100%);
        border-radius: 10px;
        padding: 4px;
        margin: 20px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .progress-bar {{
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 50%, #38BDF8 100%);
        height: 12px;
        border-radius: 8px;
        width: {progress * 100}%;
        transition: width 0.8s ease-in-out;
        position: relative;
        overflow: hidden;
    }}
    
    .progress-bar::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.3),
            transparent
        );
        animation: shimmer 2s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    
    .step-indicators {{
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        font-size: 12px;
        color: #6B7280;
    }}
    
    .step-indicator {{
        padding: 4px 8px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }}
    
    .step-completed {{
        background: #10B981;
        color: white;
        font-weight: bold;
    }}
    
    .step-current {{
        background: #2563EB;
        color: white;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
    }}
    
    .step-pending {{
        background: #E5E7EB;
        color: #6B7280;
    }}
    </style>
    
    <div class="progress-container">
        <div class="progress-bar"></div>
    </div>
    
    <div class="step-indicators">
        <span class="step-indicator {'step-completed' if current_step > 1 else 'step-current' if current_step == 1 else 'step-pending'}">
            {'✓' if current_step > 1 else '1'} Personal Info
        </span>
        <span class="step-indicator {'step-completed' if current_step > 2 else 'step-current' if current_step == 2 else 'step-pending'}">
            {'✓' if current_step > 2 else '2'} Experience
        </span>
        <span class="step-indicator {'step-completed' if current_step > 3 else 'step-current' if current_step == 3 else 'step-pending'}">
            {'✓' if current_step > 3 else '3'} Tech Stack
        </span>
        <span class="step-indicator {'step-completed' if current_step > 4 else 'step-current' if current_step == 4 else 'step-pending'}">
            {'✓' if current_step > 4 else '4'} Technical Assessment
        </span>
        <span class="step-indicator {'step-completed' if current_step > 5 else 'step-current' if current_step == 5 else 'step-pending'}">
            {'✓' if current_step > 5 else '5'} Complete
        </span>
    </div>
    """
    
    st.markdown(progress_css, unsafe_allow_html=True)

def create_tech_stack_selector() -> List[str]:
    """Create an interactive tech stack selector with chips"""
    
    # Predefined technology categories
    tech_categories = {
        "Programming Languages": [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", 
            "TypeScript", "PHP", "Ruby", "Swift", "Kotlin"
        ],
        "Frontend Frameworks": [
            "React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js"
        ],
        "Backend Frameworks": [
            "Django", "Flask", "FastAPI", "Express.js", "Spring Boot", 
            "ASP.NET", "Laravel", "Rails"
        ],
        "Databases": [
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", 
            "SQLite", "Oracle", "SQL Server"
        ],
        "Cloud & DevOps": [
            "AWS", "Google Cloud", "Azure", "Docker", "Kubernetes", 
            "Jenkins", "GitLab CI", "Terraform"
        ],
        "Tools & Others": [
            "Git", "Linux", "Nginx", "Apache", "Kafka", "RabbitMQ", 
            "GraphQL", "REST APIs"
        ]
    }
    
    selected_tech = []
    
    st.markdown("### 🛠️ Select Your Tech Stack")
    st.markdown("Choose the technologies you're experienced with:")
    
    # Create expandable sections for each category
    for category, technologies in tech_categories.items():
        with st.expander(f"📁 {category}", expanded=True):
            cols = st.columns(3)
            for i, tech in enumerate(technologies):
                with cols[i % 3]:
                    if st.checkbox(tech, key=f"tech_{tech}"):
                        selected_tech.append(tech)
    
    # Custom tech input
    st.markdown("### ➕ Add Custom Technology")
    custom_tech = st.text_input(
        "Enter any additional technologies not listed above:",
        placeholder="e.g., TensorFlow, Pandas, etc."
    )
    
    if custom_tech:
        # Split by comma and clean up
        custom_technologies = [tech.strip() for tech in custom_tech.split(',') if tech.strip()]
        selected_tech.extend(custom_technologies)
    
    # Display selected technologies as chips
    if selected_tech:
        st.markdown("### 🎯 Your Selected Tech Stack:")
        
        chips_html = """
        <style>
        .tech-chip {
            display: inline-block;
            background: linear-gradient(135deg, #2563EB, #3B82F6);
            color: white;
            padding: 6px 12px;
            margin: 4px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
            animation: chipFadeIn 0.3s ease-in;
        }
        
        @keyframes chipFadeIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .tech-chips-container {
            margin: 15px 0;
            padding: 15px;
            background: #F9FAFB;
            border-radius: 10px;
            border: 1px solid #E5E7EB;
        }
        </style>
        
        <div class="tech-chips-container">
        """
        
        for tech in selected_tech:
            chips_html += f'<span class="tech-chip">{tech}</span>'
        
        chips_html += "</div>"
        st.markdown(chips_html, unsafe_allow_html=True)
    
    return selected_tech

def create_voice_input_component() -> Optional[str]:
    """Create a voice input component (placeholder for future implementation)"""
    
    voice_css = """
    <style>
    .voice-input-container {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: 2px dashed #6366F1;
        text-align: center;
    }
    
    .voice-button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        color: white;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }
    
    .voice-button:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    
    .voice-text {
        color: #4C1D95;
        font-weight: 500;
        margin-top: 10px;
    }
    </style>
    
    <div class="voice-input-container">
        <button class="voice-button" onclick="startVoiceRecording()">🎤</button>
        <div class="voice-text">Click to use voice input</div>
        <div style="font-size: 12px; color: #6B7280; margin-top: 8px;">
            Feature coming soon! Voice recognition will be available in the next update.
        </div>
    </div>
    
    <script>
    function startVoiceRecording() {
        alert('Voice input feature is coming soon! Please use text input for now.');
    }
    </script>
    """
    
    st.markdown(voice_css, unsafe_allow_html=True)
    return None

def create_enhanced_chat_input(placeholder: str = "Type your response...") -> str:
    """Create an enhanced chat input with better styling"""
    
    input_css = """
    <style>
    .enhanced-input-container {
        background: white;
        border-radius: 12px;
        border: 2px solid #E2E8F0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 20px 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .enhanced-input-container:focus-within {
        border-color: #2563EB;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.15);
        transform: translateY(-2px);
    }
    
    .input-header {
        background: linear-gradient(90deg, #F8FAFC 0%, #F1F5F9 100%);
        padding: 8px 16px;
        border-bottom: 1px solid #E2E8F0;
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }
    
    .stTextArea > div > div > textarea {
        border: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 16px !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        resize: vertical !important;
        min-height: 100px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        box-shadow: none !important;
        outline: none !important;
    }
    </style>
    """
    
    st.markdown(input_css, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="enhanced-input-container">', unsafe_allow_html=True)
        st.markdown('<div class="input-header">💬 Your Response</div>', unsafe_allow_html=True)
        
        user_input = st.text_area(
            "",
            placeholder=placeholder,
            height=100,
            key="enhanced_chat_input",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return user_input

def create_interview_summary_export(candidate_data: Dict[str, Any]) -> None:
    """Create an export functionality for interview summary"""
    
    if st.button("📄 Export Interview Summary", type="secondary"):
        # Generate summary content
        summary_content = generate_interview_summary(candidate_data)
        
        # Create download button
        st.download_button(
            label="⬇️ Download Summary (JSON)",
            data=json.dumps(summary_content, indent=2),
            file_name=f"interview_summary_{candidate_data.get('name', 'candidate')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # Display preview
        with st.expander("📋 Preview Summary"):
            st.json(summary_content)

def generate_interview_summary(candidate_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a comprehensive interview summary"""
    
    return {
        "interview_metadata": {
            "candidate_name": candidate_data.get('name', 'Unknown'),
            "interview_date": datetime.now().isoformat(),
            "interview_duration": "Estimated 15-20 minutes",
            "interviewer": "TalentScout AI Assistant"
        },
        "candidate_profile": {
            "personal_info": {
                "name": candidate_data.get('name', ''),
                "email": candidate_data.get('email', ''),
                "phone": candidate_data.get('phone', ''),
                "location": candidate_data.get('location', '')
            },
            "professional_background": {
                "years_experience": candidate_data.get('years_experience', ''),
                "desired_positions": candidate_data.get('desired_positions', ''),
                "tech_stack": candidate_data.get('tech_stack', [])
            }
        },
        "technical_assessment": {
            "questions_asked": candidate_data.get('technical_questions', []),
            "responses_provided": candidate_data.get('technical_responses', []),
            "technologies_covered": candidate_data.get('tech_stack', [])
        },
        "summary_insights": {
            "strengths": "To be evaluated by hiring manager",
            "areas_for_discussion": "Technical depth in declared technologies",
            "next_steps": "Schedule technical interview with team lead"
        }
    }

def create_dark_mode_toggle() -> bool:
    """Create a dark mode toggle (placeholder for future implementation)"""
    
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        dark_mode = st.checkbox("🌙 Dark Mode", value=False, help="Dark mode coming soon!")
        
        if dark_mode:
            st.info("🚧 Dark mode is in development. Stay tuned for the next update!")
    
    return dark_mode

# Animation and transition utilities
def add_page_transitions() -> None:
    """Add smooth page transitions"""
    
    transition_css = """
    <style>
    .main > div {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .stButton > button {
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stSelectbox > div > div {
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input {
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        transform: scale(1.02);
    }
    </style>
    """
    
    st.markdown(transition_css, unsafe_allow_html=True)

if __name__ == "__main__":
    # Test the enhanced components
    st.title("Enhanced UI Components Demo")
    
    # Test progress bar
    create_animated_progress_bar(0.6, 5, 3)
    
    # Test tech stack selector
    selected_tech = create_tech_stack_selector()
    
    # Test voice input
    create_voice_input_component()
    
    # Test enhanced chat input
    user_input = create_enhanced_chat_input("Tell us about your experience...")
    
    # Test dark mode toggle
    create_dark_mode_toggle()
    
    # Add transitions
    add_page_transitions()
