import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Conversation, Message
from .services.chatbot_service import ChatbotService
from .utils import update_keyword_stats  # make sure this is defined


@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    """Handle incoming chat messages and return bot response."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())

        # Get or create conversation
        conversation, created = Conversation.objects.get_or_create(
            session_id=session_id
        )

        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            sender='user',
            content=user_message
        )
        update_keyword_stats(user_message)

        # Get bot response
        chatbot_service = ChatbotService()
        bot_response, source, confidence = chatbot_service.get_response(user_message, session_id)

        # Save bot message
        bot_msg = Message.objects.create(
            conversation=conversation,
            sender='bot',
            content=bot_response,
            source=source,
            confidence=confidence
        )

        return JsonResponse({
            'response': bot_response,
            'session_id': session_id,
            'source': source,
            'confidence': confidence,
            'timestamp': bot_msg.timestamp.isoformat()
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_conversation(request, session_id):
    """Get conversation history for a session."""
    try:
        conversation = Conversation.objects.get(session_id=session_id)
        messages = conversation.messages.all()

        messages_data = [{
            'sender': msg.sender,
            'content': msg.content,
            'source': msg.source,
            'confidence': msg.confidence,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]

        return JsonResponse({
            'session_id': session_id,
            'messages': messages_data
        })

    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)