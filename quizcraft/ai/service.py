"""AI service layer for interacting with language models."""

import logging
from typing import Any, Dict, List, Optional, Union

from .client import ClaudeClient
from .prompts import question_generation_prompt
from ..storage import ResponseCache

logger = logging.getLogger(__name__)

class AIService:
    """Service layer for AI-related operations with caching."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307", api_key: Optional[str] = None):
        """
        Initialize the AI service.
        
        Args:
            model: The model to use, defaults to claude-3-haiku
            api_key: Optional API key
        """
        self.client = ClaudeClient(api_key=api_key, model=model)
        self.cache = ResponseCache()
        
    def generate_questions(
        self,
        context: str,
        num_questions: int = 5,
        difficulty: str = "medium",
        cache_key_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate questions from a given context.
        
        Args:
            context: Text content to generate questions from
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            cache_key_prefix: Optional prefix for cache keys
            
        Returns:
            Dictionary containing questions and metadata
        """
        # Construct prompt
        prompt_data = question_generation_prompt.construct(
            context=context,
            num_questions=num_questions,
            difficulty=difficulty
        )
        
        # Prepare cache parameters
        cache_params = {
            "model": self.client.model,
            "num_questions": num_questions,
            "difficulty": difficulty
        }
        
        if cache_key_prefix:
            cache_params["cache_key_prefix"] = cache_key_prefix
        
        # Check cache first
        cached_response = self.cache.get(prompt_data["user_prompt"], cache_params)
        if cached_response:
            logger.info("Using cached response")
            return {
                "questions": self.client.validate_and_fix_json_response(cached_response["content"]),
                "token_usage": cached_response["usage"],
                "from_cache": True
            }
        
        # Generate response
        logger.info(f"Generating {num_questions} questions at {difficulty} difficulty...")
        response = self.client.generate_response(
            prompt=prompt_data["user_prompt"],
            system_prompt=prompt_data["system_prompt"],
            max_tokens=4000,
            temperature=0.7
        )
        
        # Cache the response
        self.cache.set(prompt_data["user_prompt"], cache_params, response)
        
        # Parse and return
        return {
            "questions": self.client.validate_and_fix_json_response(response["content"]),
            "token_usage": response["usage"],
            "from_cache": False
        }
        
    def analyze_text(self, text: str, instructions: str) -> Dict[str, Any]:
        """
        Analyze text with specific instructions.
        
        Args:
            text: The text to analyze
            instructions: Specific instructions for analysis
            
        Returns:
            Dictionary with analysis results
        
        Raises:
            NotImplementedError: This method is not yet implemented
        """
        # This is a placeholder for future milestone implementation
        raise NotImplementedError(
            "Text analysis functionality will be implemented in a future milestone"
        )