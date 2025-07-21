"""
TalentScout Hiring Assistant - Core Chatbot Module
=================================================

This module contains the main chatbot logic for conducting AI-powered
hiring interviews. It manages conversation flow, AI interactions,
sentiment analysis, and candidate data collection.

Key Features:
- Multi-stage interview process (greeting → info → tech → questions → completion)
- Google Gemini AI integration for natural conversation
- Real-time sentiment analysis during interviews
- Dynamic question generation based on candidate responses
- Comprehensive data collection and storage

Author: Your Name
Date: July 2025
"""

import os
import re
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Internal module imports
from .config import (
    EXIT_KEYWORDS, TECH_CATEGORIES, DIFFICULTY_LEVELS,
    MODEL_NAME, MAX_TOKENS, TEMPERATURE, COMPANY_NAME
)
from .data_handler import DataHandler
from .sentiment_analyzer import SentimentAnalyzer

# Load environment variables
load_dotenv()


class HiringAssistantChatbot:
    """
    Main chatbot class for conducting AI-powered hiring interviews.
    
    This class orchestrates the entire interview process, from initial greeting
    to final completion, managing conversation state, AI interactions, and
    candidate data collection throughout the journey.
    
    Attributes:
        data_handler: Manages candidate data storage and retrieval
        sentiment_analyzer: Provides real-time sentiment analysis
        conversation_history: Complete record of the conversation
        current_candidate: Current candidate's information
        conversation_stage: Current stage of the interview process
        info_step: Current step in information collection
        tech_questions_generated: Whether technical questions have been created
        session_id: Unique identifier for the current session
        sentiment_history: Historical sentiment data throughout conversation
    """
    
    def __init__(self):
        """Initialize the chatbot with all necessary components."""
        self.data_handler = DataHandler()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.conversation_history = []
        self.current_candidate = {}
        self.conversation_stage = "greeting"
        self.info_step = "name"  # Start with name collection
        self.tech_questions_generated = False
        self.session_id = None
        self.sentiment_history = []
        
        # Initialize Google Gemini AI
        self._initialize_ai()
        
        # Map conversation stages to their handler methods
        self.stages = {
            "greeting": self._handle_greeting,
            "collecting_info": self._handle_info_collection,
            "tech_stack": self._handle_tech_stack,
            "technical_questions": self._handle_technical_questions,
            "completion": self._handle_completion
        }
    
    def _initialize_ai(self) -> None:
        """Initialize Google Gemini AI with API key"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(MODEL_NAME)
    
    def _add_to_history(self, role: str, message: str) -> None:
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def _check_exit_intent(self, user_input: str) -> bool:
        """Check if user wants to exit the conversation"""
        return any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS)
    
    def _extract_info_from_response(self, response: str, field: str) -> Optional[str]:
        """Extract specific information from user response using AI"""
        prompt = f"""
        Extract the {field} from this user response: "{response}"
        
        Only return the extracted {field} value, nothing else.
        If the {field} is not found or unclear, return "NOT_FOUND".
        
        Examples:
        - For name: return just "John Smith"
        - For email: return just "john@email.com"
        - For experience: return just the number like "3" or "5"
        - For phone: return the full phone number
        """
        
        try:
            ai_response = self.model.generate_content(prompt)
            extracted = ai_response.text.strip()
            return None if extracted == "NOT_FOUND" else extracted
        except Exception as e:
            print(f"Error extracting {field}: {e}")
            return None
    
    def _handle_greeting(self, user_input: str) -> str:
        """Handle initial greeting and introduction"""
        if not hasattr(self, '_greeted'):
            self._greeted = True
            greeting_message = f"""
Hello! 👋 Welcome to {COMPANY_NAME}'s Hiring Assistant!

I'm here to help with your initial screening for technology positions. I'll be gathering some basic information about you and then asking a few technical questions based on your expertise.

This process will take about 10-15 minutes and will help our recruiters better understand your background.

To get started, could you please tell me your full name?

(You can type 'exit' or 'bye' at any time if you need to leave)
            """.strip()
            
            self._add_to_history("assistant", greeting_message)
            self.conversation_stage = "collecting_info"
            self.info_step = "name"
            return greeting_message
        
        # User has responded to greeting
        name = self._extract_info_from_response(user_input, "name")
        if name:
            self.current_candidate["name"] = name
            self.conversation_stage = "collecting_info"  # Move to next stage
            self.info_step = "email"
            response = f"Nice to meet you, {name}! Now, could you please provide your email address?"
        else:
            response = "I didn't catch your name clearly. Could you please tell me your full name?"
        
        self._add_to_history("user", user_input)
        self._add_to_history("assistant", response)
        return response
    
    def _handle_info_collection(self, user_input: str) -> str:
        """Handle systematic collection of candidate information"""
        self._add_to_history("user", user_input)
        
        if self.info_step == "name":
            # Handle name collection if somehow we end up here
            name = self._extract_info_from_response(user_input, "name")
            if name:
                self.current_candidate["name"] = name
                self.info_step = "email"
                response = f"Nice to meet you, {name}! Now, could you please provide your email address?"
            else:
                response = "I didn't catch your name clearly. Could you please tell me your full name?"
                
        elif self.info_step == "email":
            email = self._extract_info_from_response(user_input, "email")
            if email and "@" in email:
                self.current_candidate["email"] = email
                self.session_id = self.data_handler.generate_candidate_id(email)
                self.info_step = "phone"
                response = "Great! Now, what's your phone number?"
            else:
                response = "Please provide a valid email address (e.g., john@example.com)"
                
        elif self.info_step == "phone":
            phone = self._extract_info_from_response(user_input, "phone number")
            if phone:
                self.current_candidate["phone"] = phone
                self.info_step = "experience"
                response = "Perfect! How many years of professional experience do you have? (Please provide just the number)"
            else:
                response = "Could you please provide your phone number?"
                
        elif self.info_step == "experience":
            experience = self._extract_info_from_response(user_input, "years of experience")
            try:
                exp_years = int(re.findall(r'\d+', experience or user_input)[0])
                self.current_candidate["experience_years"] = exp_years
                self.info_step = "position"
                response = "Excellent! What position(s) are you interested in? (e.g., Software Engineer, Data Scientist, etc.)"
            except (ValueError, IndexError):
                response = "Please provide your years of experience as a number (e.g., 3, 5, 10)"
                
        elif self.info_step == "position":
            position = user_input.strip()
            self.current_candidate["desired_position"] = position
            self.info_step = "location"
            response = "Great choice! What's your current location or preferred work location?"
            
        elif self.info_step == "location":
            location = user_input.strip()
            self.current_candidate["location"] = location
            self.conversation_stage = "tech_stack"
            response = self._start_tech_stack_collection()
        else:
            # Default fallback if info_step is in an unexpected state
            response = "Let me get your basic information. Could you please tell me your name?"
            self.info_step = "name"
        
        self._add_to_history("assistant", response)
        return response
    
    def _start_tech_stack_collection(self) -> str:
        """Transition to tech stack collection"""
        tech_prompt = f"""
Perfect! Now I need to understand your technical background to ask relevant questions.

Please tell me about your tech stack. Include:
- Programming languages you're proficient in
- Frameworks you've worked with
- Databases you've used
- Any other tools or technologies you're comfortable with

For example: "I work with Python, Django, PostgreSQL, React, and AWS"

What technologies do you work with?
        """.strip()
        
        return tech_prompt
    
    def _handle_tech_stack(self, user_input: str) -> str:
        """Handle tech stack declaration and validation"""
        self._add_to_history("user", user_input)
        
        # Use AI to extract and categorize tech stack
        tech_stack = self._extract_tech_stack(user_input)
        
        if tech_stack:
            self.current_candidate["tech_stack"] = tech_stack
            self.current_candidate["tech_stack_raw"] = user_input
            
            # Save candidate info
            self.data_handler.save_candidate_info(self.current_candidate)
            
            # Generate technical questions
            questions = self._generate_technical_questions(tech_stack)
            self.current_candidate["technical_questions"] = questions
            
            self.conversation_stage = "technical_questions"
            self.question_index = 0
            
            confirmation = f"""
Great! I can see you work with: {', '.join(tech_stack)}

Now I'll ask you {len(questions)} technical questions to assess your proficiency. 
These questions are tailored to your experience level and the technologies you mentioned.

Let's start with the first question:

**Question 1:** {questions[0]}
            """.strip()
            
            self._add_to_history("assistant", confirmation)
            return confirmation
        else:
            response = "Could you please specify the technologies you work with? For example: Python, React, MySQL, etc."
            self._add_to_history("assistant", response)
            return response
    
    def _extract_tech_stack(self, text: str) -> List[str]:
        """Extract technology stack from user input using AI"""
        prompt = f"""
        Extract the specific technologies, programming languages, frameworks, and tools mentioned in this text: "{text}"
        
        Return only a comma-separated list of the exact technology names mentioned.
        Focus on well-known technologies like:
        - Programming languages (Python, JavaScript, Java, etc.)
        - Frameworks (React, Django, Spring, etc.)  
        - Databases (MySQL, PostgreSQL, MongoDB, etc.)
        - Cloud platforms (AWS, Azure, GCP, etc.)
        - Tools (Docker, Git, Jenkins, etc.)
        
        Example output: Python, Django, PostgreSQL, React, AWS
        
        If no clear technologies are mentioned, return "NONE".
        """
        
        try:
            response = self.model.generate_content(prompt)
            tech_list = response.text.strip()
            
            if tech_list == "NONE":
                return []
            
            # Clean and split the tech stack
            technologies = [tech.strip() for tech in tech_list.split(',') if tech.strip()]
            return technologies[:10]  # Limit to 10 technologies
            
        except Exception as e:
            print(f"Error extracting tech stack: {e}")
            return []
    
    def _generate_technical_questions(self, tech_stack: List[str]) -> List[str]:
        """Generate technical questions based on tech stack and experience"""
        experience_years = self.current_candidate.get("experience_years", 2)
        
        # Determine difficulty level
        if experience_years <= 2:
            difficulty = "beginner"
        elif experience_years <= 5:
            difficulty = "intermediate"
        else:
            difficulty = "advanced"
        
        prompt = f"""
        Generate 3-4 technical interview questions for a {difficulty} level candidate with {experience_years} years of experience.
        
        The candidate is proficient in: {', '.join(tech_stack)}
        
        Requirements:
        - Questions should be specific to the technologies mentioned
        - Appropriate for {difficulty} level ({DIFFICULTY_LEVELS[difficulty]})
        - Mix of conceptual and practical questions
        - Clear and concise
        - Focus on real-world application
        
        Format: Return only the questions, numbered 1-4, without additional text.
        
        Example format:
        1. [Question about main technology]
        2. [Question about framework/tool]
        3. [Scenario-based question]
        4. [Best practices question]
        """
        
        try:
            response = self.model.generate_content(prompt)
            questions_text = response.text.strip()
            
            # Parse questions
            questions = []
            for line in questions_text.split('\n'):
                if line.strip() and any(line.strip().startswith(str(i)) for i in range(1, 6)):
                    # Remove number prefix and clean
                    question = re.sub(r'^\d+\.?\s*', '', line.strip())
                    if question:
                        questions.append(question)
            
            return questions[:4]  # Return max 4 questions
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            # Fallback questions
            return [
                f"Can you explain a challenging project you worked on using {tech_stack[0] if tech_stack else 'your main technology'}?",
                "How do you approach debugging when you encounter a difficult bug?",
                "What's your experience with version control and team collaboration?"
            ]
    
    def _handle_technical_questions(self, user_input: str) -> str:
        """Handle technical question responses"""
        self._add_to_history("user", user_input)
        
        questions = self.current_candidate.get("technical_questions", [])
        
        # Store the response
        if "technical_responses" not in self.current_candidate:
            self.current_candidate["technical_responses"] = {}
        
        question_key = f"question_{self.question_index + 1}"
        self.current_candidate["technical_responses"][question_key] = user_input
        
        # Move to next question or completion
        self.question_index += 1
        
        if self.question_index < len(questions):
            # Ask next question
            response = f"""
Thank you for your answer!

**Question {self.question_index + 1}:** {questions[self.question_index]}
            """.strip()
        else:
            # All questions answered, move to completion
            self.conversation_stage = "completion"
            response = self._handle_completion(user_input="")
        
        self._add_to_history("assistant", response)
        return response
    
    def _handle_completion(self, user_input: str) -> str:
        """Handle conversation completion"""
        # Save final data
        self.data_handler.update_candidate_responses(
            self.session_id, 
            self.current_candidate.get("technical_responses", {})
        )
        self.data_handler.mark_session_complete(self.session_id)
        
        completion_message = f"""
Excellent! That completes our initial screening process. Thank you for taking the time to speak with me today, {self.current_candidate.get('name', 'there')}!

📋 **Summary:**
- Name: {self.current_candidate.get('name')}
- Position Interest: {self.current_candidate.get('desired_position')}
- Experience: {self.current_candidate.get('experience_years')} years
- Tech Stack: {', '.join(self.current_candidate.get('tech_stack', []))}
- Questions Answered: {len(self.current_candidate.get('technical_responses', {}))}

🔄 **Next Steps:**
1. Our recruitment team will review your responses
2. You'll hear back from us within 2-3 business days
3. If there's a good fit, we'll schedule a more detailed interview

📞 **Contact:** 
If you have any questions, feel free to reach out using the contact information you provided.

Thank you for your interest in {COMPANY_NAME}! Have a great day! 🌟

        """.strip()
        
        self._add_to_history("assistant", completion_message)
        return completion_message
    
    def process_message(self, user_input: str) -> str:
        """
        Main method to process user input and return chatbot response
        
        Args:
            user_input: User's message
            
        Returns:
            Chatbot's response
        """
        if not user_input.strip():
            return "I didn't receive any input. Could you please say something?"
        
        # Analyze sentiment for candidate responses
        if self.conversation_stage != "greeting" and user_input.strip():
            sentiment = self.sentiment_analyzer.analyze_response(user_input)
            self.sentiment_history.append({
                'timestamp': datetime.now().isoformat(),
                'sentiment': sentiment,
                'user_input': user_input,
                'stage': self.conversation_stage
            })
        
        # Check for exit intent
        if self._check_exit_intent(user_input):
            return self._handle_exit()
        
        # Handle based on current conversation stage
        handler = self.stages.get(self.conversation_stage, self._handle_fallback)
        return handler(user_input)
    
    def _handle_exit(self) -> str:
        """Handle user exit request"""
        if self.session_id and self.current_candidate:
            # Save partial data
            self.data_handler.save_candidate_info(self.current_candidate)
        
        return f"""
Thank you for your time with {COMPANY_NAME}'s Hiring Assistant! 

If you'd like to complete the screening process later, please feel free to return and start a new session.

Have a great day! 👋
        """.strip()
    
    def _handle_fallback(self, user_input: str) -> str:
        """Handle unexpected inputs or errors"""
        fallback_prompt = f"""
        The user said: "{user_input}"
        
        This seems to be outside the scope of a hiring conversation. 
        Please provide a polite response that redirects them back to the hiring process.
        Keep it brief and professional.
        
        Current conversation stage: {self.conversation_stage}
        """
        
        try:
            response = self.model.generate_content(fallback_prompt)
            fallback_response = response.text.strip()
        except:
            fallback_response = "I'm here to help with your job application. Could you please provide the information I requested?"
        
        self._add_to_history("user", user_input)
        self._add_to_history("assistant", fallback_response)
        return fallback_response
    
    def get_conversation_history(self) -> List[Dict]:
        """Return conversation history"""
        return self.conversation_history
    
    def get_candidate_info(self) -> Dict:
        """Return current candidate information"""
        return self.current_candidate.copy()
    
    def get_current_sentiment(self) -> Dict[str, Any]:
        """Get the most recent sentiment analysis"""
        if not self.sentiment_history:
            return {
                'confidence_level': '50%',
                'primary_emotion': 'Neutral',
                'overall_sentiment': 'Neutral',
                'engagement': 'Medium'
            }
        
        latest_sentiment = self.sentiment_history[-1]['sentiment']
        return self.sentiment_analyzer.get_sentiment_summary(latest_sentiment)
    
    def get_sentiment_history(self) -> List[Dict]:
        """Get complete sentiment history"""
        return self.sentiment_history.copy()
    
    def reset_conversation(self) -> None:
        """Reset conversation state for new session"""
        self.conversation_history = []
        self.current_candidate = {}
        self.conversation_stage = "greeting"
        self.tech_questions_generated = False
        self.session_id = None
        if hasattr(self, '_greeted'):
            delattr(self, '_greeted')
