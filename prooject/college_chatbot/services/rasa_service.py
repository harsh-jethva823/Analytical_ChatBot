import requests
import json
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class RasaService:
    """Service for interacting with Rasa chatbot."""
    
    def __init__(self):
        self.rasa_url = "http://localhost:5005"  # Default Rasa server URL
        self.webhook_url = f"{self.rasa_url}/webhooks/rest/webhook"
        
    def get_response(self, message: str, sender_id: str) -> Tuple[Optional[str], float]:
        """
        Get response from Rasa.
        
        Returns:
            Tuple of (response_text, confidence)
        """
        try:
            # Check if Rasa server is running
            if not self._is_rasa_running():
                logger.warning("Rasa server is not running")
                return None, 0.0
            
            payload = {
                "sender": sender_id,
                "message": message
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0:
                    # Get the first response
                    bot_message = data[0].get('text', '')
                    # Rasa doesn't always provide confidence, so we estimate it
                    confidence = self._estimate_confidence(bot_message)
                    return bot_message, confidence
                    
            logger.warning(f"Rasa returned status code: {response.status_code}")
            return None, 0.0
            
        except requests.exceptions.ConnectionError:
            logger.warning("Cannot connect to Rasa server")
            return None, 0.0
        except requests.exceptions.Timeout:
            logger.warning("Rasa server timeout")
            return None, 0.0
        except Exception as e:
            logger.error(f"Error communicating with Rasa: {e}")
            return None, 0.0
    
    def _is_rasa_running(self) -> bool:
        """Check if Rasa server is running."""
        try:
            response = requests.get(f"{self.rasa_url}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _estimate_confidence(self, response: str) -> float:
        """
        Estimate confidence based on response characteristics.
        This is a simple heuristic since Rasa webhook doesn't always return confidence.
        """
        if not response:
            return 0.0
        
        # Simple heuristics for confidence estimation
        if "I'm not sure" in response.lower() or "I don't know" in response.lower():
            return 0.3
        elif len(response) < 20:  # Very short responses might be less confident
            return 0.6
        elif any(keyword in response.lower() for keyword in ['specific', 'detailed', 'information']):
            return 0.8
        else:
            return 0.7  # Default confidence for normal responses