"""
CSS Styles for TalentScout Hiring Assistant
Contains all the styling for the Streamlit application
"""

def get_main_css():
    """Return the main CSS styles for the application"""
    return """
<style>
    /* Modern color palette and typography - Updated Color Scheme */
    :root {
        --primary-color: #2563EB;
        --primary-hover: #1D4ED8;
        --secondary-color: #38BDF8;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --bg-page: #F9FAFB;
        --bg-card: #FFFFFF;
        --bg-sidebar: #E0F2FE;
        --success-color: #059669;
        --success-light: #d1fae5;
        --warning-color: #d97706;
        --warning-light: #fef3c7;
        --border-color: #E5E7EB;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }

    /* Clean modern background */
    .stApp {
        background: var(--bg-page) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Enhanced header with new color scheme */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
        color: white;
        text-align: center;
        padding: 2rem 0;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    .main-header h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1.1rem !important;
        opacity: 0.9;
        color: white !important;
        margin: 0 !important;
    }

    /* Modern chat message styling with better UX */
    .user-message {
        background: linear-gradient(135deg, var(--primary-light) 0%, #bfdbfe 100%);
        padding: 1.25rem;
        border-radius: 18px 18px 4px 18px;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-color);
        box-shadow: var(--shadow-sm);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: linear-gradient(135deg, var(--success-light) 0%, #bbf7d0 100%);
        padding: 1.25rem;
        border-radius: 18px 18px 18px 4px;
        margin: 1rem 0;
        border-left: 4px solid var(--success-color);
        box-shadow: var(--shadow-sm);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Enhanced info card */
    .info-card {
        background: linear-gradient(135deg, #ffffff 0%, var(--bg-secondary) 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid var(--border-color);
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: var(--shadow-md);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .info-card h2 {
        color: var(--text-primary) !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }

    /* Improved text styling */
    .stMarkdown, .stMarkdown *, div[data-testid="stMarkdownContainer"] * {
        color: var(--text-primary) !important;
        line-height: 1.6 !important;
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* Modern sidebar design */
    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    section[data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: var(--primary-color) !important;
    }

    /* Enhanced input styling */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }

    /* Modern text area styling */
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        caret-color: var(--primary-color) !important;
        transition: all 0.2s ease !important;
        resize: vertical !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    /* Disabled textarea styling - ensuring black text */
    textarea:disabled {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        cursor: not-allowed !important;
        opacity: 1 !important;
        border-color: var(--border-color) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stTextArea textarea:disabled,
    .stTextArea > div > div > textarea:disabled,
    div[data-testid="stTextArea"] textarea:disabled,
    textarea[disabled],
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextArea"] textarea:disabled {
        color: #000000 !important;
        background-color: #f8f9fa !important;
    }

    /* Clean white chat input styling */
    .stChatInput {
        background: white !important;
        border-radius: 12px !important;
        padding: 0.25rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid #e5e7eb !important;
        margin: 1rem 0 !important;
    }
    
    .stChatInput > div > div > input {
        background-color: white !important;
        color: #374151 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        caret-color: #374151 !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
        color: #000000 !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, var(--primary-color) 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInput button:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Modern button styling with new color scheme */
    .stButton > button {
        border-radius: 12px !important;
        border: 2px solid var(--border-color) !important;
        padding: 0.75rem 1.5rem !important;
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
        border-color: var(--secondary-color) !important;
        background: var(--bg-sidebar) !important;
        color: var(--text-primary) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button[kind="primary"]:before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.5s !important;
    }

    .stButton > button[kind="primary"]:hover:before {
        left: 100% !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-hover) 0%, var(--secondary-color) 100%) !important;
        border-color: var(--primary-hover) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0) scale(0.98) !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
    }

    /* Enhanced sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        margin: 0.25rem 0 !important;
    }

    /* Modern progress bar with new colors */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        border-radius: 8px !important;
    }
    
    .stProgress > div > div {
        background-color: var(--bg-page) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        height: 12px !important;
    }

    /* Responsive spacing */
    .main {
        padding: 1rem 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    /* Enhanced dividers */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent 0%, var(--border-color) 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }

    /* Loading spinner enhancement */
    .stSpinner {
        color: var(--primary-color) !important;
    }

    /* Enhanced form styling for response input with new colors */
    .stTextInput > div > div > input {
        background-color: var(--bg-card) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
        height: 48px !important;
        line-height: 1.4 !important;
        vertical-align: middle !important;
        display: flex !important;
        align-items: center !important;
        caret-color: var(--primary-color) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
        caret-color: var(--primary-color) !important;
    }
    
    /* Fix text input container alignment */
    .stTextInput > div {
        display: flex !important;
        align-items: center !important;
    }
    
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* Enhanced form submit button styling with animations */
    .stForm > div:last-child button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        height: 48px !important;
        margin-top: 0 !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .stForm > div:last-child button[kind="primary"]:before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.5s !important;
    }

    .stForm > div:last-child button[kind="primary"]:hover:before {
        left: 100% !important;
    }
    
    .stForm > div:last-child button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        background: linear-gradient(135deg, var(--primary-hover) 0%, var(--secondary-color) 100%) !important;
        border-color: var(--primary-hover) !important;
    }

    .stForm > div:last-child button[kind="primary"]:active {
        transform: translateY(0) scale(0.98) !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
    }

    /* Additional selectors for form submit buttons to ensure animations work */
    .stForm button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        border: 2px solid var(--primary-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        height: 48px !important;
        margin-top: 0 !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .stForm button[kind="primary"]:before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.5s !important;
    }

    .stForm button[kind="primary"]:hover:before {
        left: 100% !important;
    }
    
    .stForm button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        background: linear-gradient(135deg, var(--primary-hover) 0%, var(--secondary-color) 100%) !important;
        border-color: var(--primary-hover) !important;
    }

    .stForm button[kind="primary"]:active {
        transform: translateY(0) scale(0.98) !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Ensure form elements are properly aligned */
    .stForm > div {
        display: flex !important;
        align-items: flex-end !important;
        gap: 0.5rem !important;
    }
    
    .stForm [data-testid="column"] {
        display: flex !important;
        align-items: flex-end !important;
    }

    /* Cards and panels styling */
    .stContainer, .stColumn {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-sm) !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }

    /* Chat message styling */
    .stChatMessage {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-sm) !important;
        margin: 0.5rem 0 !important;
        padding: 1rem !important;
    }

    /* Metric containers */
    .metric-container {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-sm) !important;
        padding: 1rem !important;
    }

    /* Ensure muted text uses secondary color */
    .text-muted, .stMarkdown p small, .help-text {
        color: var(--text-secondary) !important;
    }

    /* Ensure headers use primary color */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color) !important;
    }
</style>
"""
