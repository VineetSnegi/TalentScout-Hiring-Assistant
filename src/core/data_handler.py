"""
Data handling utilities for TalentScout Hiring Assistant
Manages candidate information storage and retrieval
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
from .config import DATA_DIR, CANDIDATES_FILE


class DataHandler:
    """Handles secure storage and retrieval of candidate data"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.candidates_file = os.path.join(self.data_dir, CANDIDATES_FILE)
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_candidates(self) -> List[Dict]:
        """Load existing candidate data from JSON file"""
        if not os.path.exists(self.candidates_file):
            return []
        
        try:
            with open(self.candidates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_candidates(self, candidates: List[Dict]) -> None:
        """Save candidate data to JSON file"""
        try:
            with open(self.candidates_file, 'w', encoding='utf-8') as f:
                json.dump(candidates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving candidate data: {e}")
    
    def generate_candidate_id(self, email: str) -> str:
        """Generate unique candidate ID based on email hash"""
        return hashlib.md5(email.lower().encode()).hexdigest()[:8]
    
    def save_candidate_info(self, candidate_data: Dict[str, Any]) -> bool:
        """
        Save candidate information securely
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            bool: Success status
        """
        try:
            candidates = self._load_candidates()
            
            # Add metadata
            candidate_data['id'] = self.generate_candidate_id(candidate_data.get('email', ''))
            candidate_data['timestamp'] = datetime.now().isoformat()
            candidate_data['session_completed'] = False
            
            # Check if candidate already exists
            existing_index = -1
            for i, candidate in enumerate(candidates):
                if candidate.get('id') == candidate_data['id']:
                    existing_index = i
                    break
            
            if existing_index >= 0:
                # Update existing candidate
                candidates[existing_index].update(candidate_data)
            else:
                # Add new candidate
                candidates.append(candidate_data)
            
            self._save_candidates(candidates)
            return True
            
        except Exception as e:
            print(f"Error saving candidate info: {e}")
            return False
    
    def get_candidate_info(self, candidate_id: str) -> Optional[Dict]:
        """Retrieve candidate information by ID"""
        candidates = self._load_candidates()
        for candidate in candidates:
            if candidate.get('id') == candidate_id:
                return candidate
        return None
    
    def update_candidate_responses(self, candidate_id: str, responses: Dict[str, str]) -> bool:
        """Update candidate's technical question responses"""
        try:
            candidates = self._load_candidates()
            
            for candidate in candidates:
                if candidate.get('id') == candidate_id:
                    if 'technical_responses' not in candidate:
                        candidate['technical_responses'] = {}
                    candidate['technical_responses'].update(responses)
                    candidate['last_updated'] = datetime.now().isoformat()
                    break
            
            self._save_candidates(candidates)
            return True
            
        except Exception as e:
            print(f"Error updating responses: {e}")
            return False
    
    def mark_session_complete(self, candidate_id: str) -> bool:
        """Mark candidate session as completed"""
        try:
            candidates = self._load_candidates()
            
            for candidate in candidates:
                if candidate.get('id') == candidate_id:
                    candidate['session_completed'] = True
                    candidate['completion_time'] = datetime.now().isoformat()
                    break
            
            self._save_candidates(candidates)
            return True
            
        except Exception as e:
            print(f"Error marking session complete: {e}")
            return False
    
    def get_all_candidates(self) -> List[Dict]:
        """Retrieve all candidate records"""
        return self._load_candidates()
    
    def get_candidates_summary(self) -> pd.DataFrame:
        """Get summary statistics of candidates"""
        candidates = self._load_candidates()
        if not candidates:
            return pd.DataFrame()
        
        df = pd.DataFrame(candidates)
        return df[['name', 'email', 'experience_years', 'desired_position', 
                  'tech_stack', 'session_completed', 'timestamp']]
    
    def anonymize_candidate_data(self, candidate_id: str) -> bool:
        """Anonymize sensitive candidate information"""
        try:
            candidates = self._load_candidates()
            
            for candidate in candidates:
                if candidate.get('id') == candidate_id:
                    # Replace sensitive data with anonymized versions
                    candidate['name'] = f"Candidate_{candidate_id}"
                    candidate['email'] = f"candidate_{candidate_id}@anonymous.com"
                    candidate['phone'] = "XXX-XXX-XXXX"
                    candidate['anonymized'] = True
                    candidate['anonymized_date'] = datetime.now().isoformat()
                    break
            
            self._save_candidates(candidates)
            return True
            
        except Exception as e:
            print(f"Error anonymizing data: {e}")
            return False
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """Remove candidate data older than specified days"""
        try:
            candidates = self._load_candidates()
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            initial_count = len(candidates)
            candidates = [
                candidate for candidate in candidates
                if datetime.fromisoformat(candidate.get('timestamp', datetime.now().isoformat())) > cutoff_date
            ]
            
            self._save_candidates(candidates)
            return initial_count - len(candidates)
            
        except Exception as e:
            print(f"Error cleaning up old sessions: {e}")
            return 0
    
    def validate_candidate_data(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate candidate data for completeness and format
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        required_fields = ['name', 'email', 'phone', 'experience_years', 'desired_position']
        
        # Check required fields
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate email format
        email = data.get('email', '')
        if email and '@' not in email:
            errors.append("Invalid email format")
        
        # Validate experience years
        try:
            years = int(data.get('experience_years', 0))
            if years < 0 or years > 50:
                errors.append("Experience years must be between 0 and 50")
        except (ValueError, TypeError):
            errors.append("Experience years must be a valid number")
        
        # Validate phone (basic check)
        phone = data.get('phone', '')
        if phone and len(phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')) < 10:
            errors.append("Phone number appears to be too short")
        
        return len(errors) == 0, errors
    
    def export_candidates_csv(self, filepath: str = None) -> str:
        """Export candidate data to CSV file"""
        try:
            df = self.get_candidates_summary()
            if df.empty:
                return "No candidate data to export"
            
            if not filepath:
                filepath = os.path.join(self.data_dir, f"candidates_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            
            df.to_csv(filepath, index=False)
            return f"Data exported to: {filepath}"
            
        except Exception as e:
            return f"Error exporting data: {e}"


# Utility functions for data handling
def mask_sensitive_info(text: str, mask_char: str = '*') -> str:
    """Mask sensitive information in text"""
    if len(text) <= 4:
        return mask_char * len(text)
    return text[:2] + mask_char * (len(text) - 4) + text[-2:]


def is_valid_email(email: str) -> bool:
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]


def format_phone_number(phone: str) -> str:
    """Format phone number consistently"""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone
