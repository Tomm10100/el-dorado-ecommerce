"""
AI Tutor package for InnovLead Education Bot
Integrates with Anthropic Claude or OpenAI for educational assistance
"""
from .tutor_engine import AITutor, get_ai_tutor

__all__ = ['AITutor', 'get_ai_tutor']
