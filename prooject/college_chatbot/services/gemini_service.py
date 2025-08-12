import google.generativeai as genai
import logging
from django.conf import settings
from typing import Optional

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google's Gemini AI."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key and self.api_key != 'AIzaSyCOYJIhNLGDZ5WHKyydveQ2UU0__SC92eM':
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.is_configured = True
        else:
            self.is_configured = False
            logger.warning("Gemini API key not configured")
    
    def get_response(self, message: str) -> Optional[str]:
        """
        Get response from Gemini AI with college-specific context.
        
        Returns:
            Response text or None if error
        """
        if not self.is_configured:
            return "I'm sorry, but I'm currently unable to process your request. Please try again later or contact our admissions office."
        
        try:
            # Create a college-specific prompt
            college_context = """
            You are a helpful college inquiry chatbot for a university. You help prospective students 
            and their families with questions about admissions, courses, campus life, fees, scholarships, 
            facilities, and other college-related topics.
            
            Keep your responses helpful, informative, and encouraging. If you don't have specific 
            information about the college, provide general guidance and suggest contacting the 
            admissions office for detailed information.
            
            Student question: {message}
            
            Please provide a helpful response as a college inquiry chatbot:
            """
            
            prompt = college_context.format(message=message)
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response")
                return None
                
        except Exception as e:
            logger.error(f"Error with Gemini AI: {e}")
            return None