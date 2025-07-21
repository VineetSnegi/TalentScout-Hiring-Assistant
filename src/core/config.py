"""
Configuration settings for TalentScout Hiring Assistant
"""

import os
from typing import List, Dict

# Application Configuration
APP_TITLE = "TalentScout - Hiring Assistant"
APP_ICON = "🤖"
COMPANY_NAME = "TalentScout"

# Conversation Settings
MAX_CONVERSATION_HISTORY = 20
SESSION_TIMEOUT_MINUTES = 30

# Exit Keywords - More specific to avoid false positives
EXIT_KEYWORDS = [
    "bye", "goodbye", "exit", "quit", "end conversation", "stop interview", 
    "terminate", "close interview", "i want to exit", "i want to quit"
]

# Tech Stack Categories
TECH_CATEGORIES = {
    "Programming Languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust",
        "TypeScript", "PHP", "Ruby", "Swift", "Kotlin", "Scala"
    ],
    "Frontend Frameworks": [
        "React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js",
        "Bootstrap", "Tailwind CSS", "Material-UI"
    ],
    "Backend Frameworks": [
        "Django", "Flask", "FastAPI", "Express.js", "Spring Boot",
        "Laravel", "Ruby on Rails", "ASP.NET", "Gin", "Fiber"
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
        "Oracle", "SQL Server", "Cassandra", "DynamoDB"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins",
        "GitLab CI", "Terraform", "Ansible"
    ],
    "Data Science & AI": [
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
        "Jupyter", "Apache Spark", "Kafka"
    ]
}

# Question Difficulty Levels
DIFFICULTY_LEVELS = {
    "beginner": "0-2 years experience",
    "intermediate": "2-5 years experience", 
    "advanced": "5+ years experience"
}

# Data Storage
DATA_DIR = "data"
CANDIDATES_FILE = "candidates.json"

# UI Configuration
SIDEBAR_WIDTH = 300
CHAT_HEIGHT = 400

# Model Configuration
MODEL_NAME = "gemini-1.5-flash"  # Updated to current available model
MAX_TOKENS = 1000
TEMPERATURE = 0.7
