"""
AI Tutor Engine - Educational AI powered by Claude or OpenAI
Non-commercial filter ensures educational responses only
"""
from typing import Optional
import anthropic
import openai
from config import get_settings
from .prompt_templates import SYSTEM_PROMPT, NON_COMMERCIAL_FILTER

settings = get_settings()


class AITutor:
    """AI Tutor for educational assistance"""
    
    def __init__(self):
        self.settings = settings
        self.provider = settings.ai_provider
        
        if self.provider == 'anthropic' and settings.anthropic_api_key:
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            self.model = settings.anthropic_model
        elif self.provider == 'openai' and settings.openai_api_key:
            openai.api_key = settings.openai_api_key
            self.model = settings.openai_model
        else:
            raise ValueError("No valid AI provider configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env")
    
    def ask(self, user_question: str, context: Optional[str] = None) -> str:
        """
        Ask the AI tutor a question
        
        Args:
            user_question: The user's question
            context: Optional context (e.g., current lesson content)
            
        Returns:
            AI tutor's response
        """
        try:
            # Build the full prompt
            full_prompt = self._build_prompt(user_question, context)
            
            # Get response based on provider
            if self.provider == 'anthropic':
                response = self._ask_claude(full_prompt)
            else:
                response = self._ask_openai(full_prompt)
            
            # Apply non-commercial filter
            filtered_response = self._apply_filter(response)
            
            return filtered_response
        
        except Exception as e:
            return f"I apologize, but I'm having technical difficulties right now. Please try again later or contact {settings.org_email} for assistance."
    
    def _build_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Build the full prompt with system instructions"""
        prompt_parts = [SYSTEM_PROMPT]
        
        if context:
            prompt_parts.append(f"\n**Current Lesson Context:**\n{context}\n")
        
        prompt_parts.append(f"\n**User Question:**\n{question}")
        
        return "\n".join(prompt_parts)
    
    def _ask_claude(self, prompt: str) -> str:
        """Get response from Claude"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def _ask_openai(self, prompt: str) -> str:
        """Get response from OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _apply_filter(self, response: str) -> str:
        """
        Apply non-commercial filter to ensure educational responses
        Checks for commercial language and adds disclaimers if needed
        """
        # Keywords that suggest commercial intent
        commercial_keywords = [
            'hire', 'consulting', 'service', 'paid', 'purchase',
            'buy', 'sale', 'pricing', 'quote', 'proposal'
        ]
        
        response_lower = response.lower()
        
        # Check if response contains commercial language
        contains_commercial = any(keyword in response_lower for keyword in commercial_keywords)
        
        if contains_commercial or 'professional service' in response_lower:
            # Add educational disclaimer
            disclaimer = f"\n\n{NON_COMMERCIAL_FILTER}"
            return response + disclaimer
        
        return response


# Global AI tutor instance
_ai_tutor: Optional[AITutor] = None


def get_ai_tutor() -> AITutor:
    """Get or create AI tutor instance (singleton pattern)"""
    global _ai_tutor
    if _ai_tutor is None and settings.enable_ai_tutor:
        _ai_tutor = AITutor()
    return _ai_tutor
