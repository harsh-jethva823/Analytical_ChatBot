import requests
import json
import logging
from typing import Tuple
from .rasa_service import RasaService
from .gemini_service import GeminiService

logger = logging.getLogger(__name__)


class ChatbotService:
    """Main chatbot service that coordinates between Rasa and Gemini AI."""
    
    def __init__(self):
        self.rasa_service = RasaService()
        self.gemini_service = GeminiService()
        self.confidence_threshold = 0.6  # Minimum confidence for Rasa responses
    
    def get_response(self, message: str, session_id: str) -> Tuple[str, str, float]:
        """
        Get response from chatbot, trying Rasa first, then Gemini as fallback.
        
        Returns:
            Tuple of (response_text, source, confidence)
        """
        try:
            # Try Rasa first
            rasa_response, confidence = self.rasa_service.get_response(message, session_id)
            
            if rasa_response and confidence >= self.confidence_threshold:
                logger.info(f"Rasa response with confidence {confidence}: {rasa_response}")
                return rasa_response, 'rasa', confidence
            
            # Fall back to Gemini if Rasa confidence is low or no response
            logger.info(f"Rasa confidence too low ({confidence}), falling back to Gemini")
            gemini_response = self.gemini_service.get_response(message)
            
            if gemini_response:
                return gemini_response, 'gemini', 1.0
            
            # Ultimate fallback
            return self._get_fallback_response(message), 'fallback', 0.5
            
        except Exception as e:
            logger.error(f"Error in chatbot service: {e}")
            return self._get_fallback_response(message), 'fallback', 0.0
    
    def _get_fallback_response(self, message: str) -> str:
        """Return a generic fallback response."""
        fallback_responses = [
            "I'm sorry, I didn't understand that. Could you please rephrase your question about our college?",
            "I'm not sure about that. Can you ask me something specific about admissions, courses, or campus life?",
            "That's an interesting question! For detailed information, please contact our admissions office or visit our website.",
            "I'd be happy to help with questions about our college programs, admission requirements, or campus facilities."
        ]
        
        # Simple hash-based selection for consistency
        index = hash(message) % len(fallback_responses)
        return fallback_responses[index]