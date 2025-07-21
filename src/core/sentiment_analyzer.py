"""
Sentiment Analysis Module for TalentScout Hiring Assistant
Analyzes candidate emotions and confidence levels during interviews
"""

import re
from typing import Dict, Tuple, List
from dataclasses import dataclass

@dataclass
class SentimentMetrics:
    """Data class for sentiment analysis results"""
    confidence_score: float  # 0.0 to 1.0
    emotion_category: str   # 'confident', 'nervous', 'neutral', 'excited'
    stress_indicators: List[str]
    positive_indicators: List[str]
    overall_sentiment: str  # 'positive', 'negative', 'neutral'

class SentimentAnalyzer:
    """Analyzes candidate sentiment and emotional state during interviews"""
    
    def __init__(self):
        self.confidence_keywords = {
            'high': ['confident', 'sure', 'definitely', 'absolutely', 'experienced', 'expert', 'proficient'],
            'medium': ['think', 'believe', 'probably', 'likely', 'familiar', 'comfortable'],
            'low': ['unsure', 'maybe', 'not sure', 'don\'t know', 'uncertain', 'confused']
        }
        
        self.emotion_patterns = {
            'nervous': ['um', 'uh', 'well...', 'i guess', 'not really sure'],
            'excited': ['love', 'enjoy', 'passion', 'amazing', 'fantastic', 'excited'],
            'frustrated': ['difficult', 'hard', 'challenging', 'struggle', 'problem'],
            'confident': ['experienced', 'skilled', 'accomplished', 'successful', 'expertise']
        }
        
        self.stress_indicators = [
            r'\b(um|uh|well|like)\b',  # Filler words
            r'\.{3,}',  # Multiple dots (hesitation)
            r'\?\?+',   # Multiple question marks (uncertainty)
            r'I don\'t know',
            r'not sure',
            r'maybe'
        ]

    def analyze_response(self, text: str) -> SentimentMetrics:
        """
        Analyze the sentiment of a candidate's response
        
        Args:
            text: The candidate's response text
            
        Returns:
            SentimentMetrics object with analysis results
        """
        text_lower = text.lower()
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(text_lower)
        
        # Detect emotions
        emotion_category = self._detect_primary_emotion(text_lower)
        
        # Find stress indicators
        stress_indicators = self._find_stress_indicators(text)
        
        # Find positive indicators
        positive_indicators = self._find_positive_indicators(text_lower)
        
        # Overall sentiment
        overall_sentiment = self._determine_overall_sentiment(
            confidence_score, len(stress_indicators), len(positive_indicators)
        )
        
        return SentimentMetrics(
            confidence_score=confidence_score,
            emotion_category=emotion_category,
            stress_indicators=stress_indicators,
            positive_indicators=positive_indicators,
            overall_sentiment=overall_sentiment
        )

    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence level based on language patterns"""
        confidence_score = 0.5  # Start neutral
        
        # High confidence indicators
        for keyword in self.confidence_keywords['high']:
            if keyword in text:
                confidence_score += 0.15
        
        # Medium confidence indicators
        for keyword in self.confidence_keywords['medium']:
            if keyword in text:
                confidence_score += 0.05
        
        # Low confidence indicators
        for keyword in self.confidence_keywords['low']:
            if keyword in text:
                confidence_score -= 0.2
        
        # Length and completeness (longer, detailed responses = more confidence)
        if len(text.split()) > 50:
            confidence_score += 0.1
        elif len(text.split()) < 10:
            confidence_score -= 0.1
        
        return max(0.0, min(1.0, confidence_score))

    def _detect_primary_emotion(self, text: str) -> str:
        """Detect the primary emotion in the response"""
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text)
            if score > 0:
                emotion_scores[emotion] = score
        
        if not emotion_scores:
            return 'neutral'
        
        return max(emotion_scores, key=emotion_scores.get)

    def _find_stress_indicators(self, text: str) -> List[str]:
        """Find indicators of stress or nervousness"""
        indicators = []
        
        for pattern in self.stress_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        return indicators

    def _find_positive_indicators(self, text: str) -> List[str]:
        """Find positive sentiment indicators"""
        positive_words = ['enjoy', 'love', 'passion', 'excited', 'accomplished', 
                         'successful', 'proud', 'confident', 'skilled', 'experienced']
        
        indicators = []
        for word in positive_words:
            if word in text:
                indicators.append(word)
        
        return indicators

    def _determine_overall_sentiment(self, confidence: float, stress_count: int, positive_count: int) -> str:
        """Determine overall sentiment based on various factors"""
        if confidence > 0.7 and positive_count > stress_count:
            return 'positive'
        elif confidence < 0.3 or stress_count > positive_count + 2:
            return 'negative'
        else:
            return 'neutral'

    def generate_feedback_prompt(self, sentiment: SentimentMetrics) -> str:
        """
        Generate appropriate interviewer response based on sentiment analysis
        
        Args:
            sentiment: SentimentMetrics from analysis
            
        Returns:
            Suggested prompt adjustment for the AI interviewer
        """
        if sentiment.emotion_category == 'nervous' or sentiment.confidence_score < 0.4:
            return "The candidate seems nervous. Use encouraging language and provide reassurance."
        
        elif sentiment.emotion_category == 'confident' and sentiment.confidence_score > 0.8:
            return "The candidate is very confident. You can ask more challenging follow-up questions."
        
        elif sentiment.emotion_category == 'frustrated':
            return "The candidate may be struggling. Offer to clarify or move to a different topic."
        
        elif sentiment.emotion_category == 'excited':
            return "The candidate is enthusiastic. You can explore their passion areas in more depth."
        
        else:
            return "Continue with normal interview flow."

    def get_sentiment_summary(self, sentiment: SentimentMetrics) -> Dict[str, str]:
        """Get a formatted summary of sentiment analysis for display"""
        return {
            'confidence_level': f"{sentiment.confidence_score:.1%}",
            'primary_emotion': sentiment.emotion_category.title(),
            'overall_sentiment': sentiment.overall_sentiment.title(),
            'stress_level': 'High' if len(sentiment.stress_indicators) > 3 else 
                          'Medium' if len(sentiment.stress_indicators) > 1 else 'Low',
            'engagement': 'High' if len(sentiment.positive_indicators) > 2 else
                         'Medium' if len(sentiment.positive_indicators) > 0 else 'Low'
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Test responses
    test_responses = [
        "I'm very confident in my Python skills and have 5 years of experience building web applications.",
        "Um, well, I think I know Python but I'm not really sure about Django...",
        "I absolutely love working with React! It's amazing how flexible it is.",
        "This is really difficult. I'm not sure I understand the question."
    ]
    
    for response in test_responses:
        sentiment = analyzer.analyze_response(response)
        summary = analyzer.get_sentiment_summary(sentiment)
        print(f"Response: {response[:50]}...")
        print(f"Analysis: {summary}")
        print(f"Feedback: {analyzer.generate_feedback_prompt(sentiment)}")
        print("-" * 50)
