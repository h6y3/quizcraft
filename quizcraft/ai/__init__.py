"""AI module for interacting with the Anthropic Claude API."""

from .client import ClaudeClient
from .credentials import get_api_key, load_api_credentials
from .prompts import PromptTemplate, QuestionGenerationPrompt, question_generation_prompt
from .service import AIService
from .tokens import estimate_token_count, optimize_context

__all__ = [
    "AIService",
    "ClaudeClient",
    "get_api_key",
    "load_api_credentials",
    "estimate_token_count",
    "optimize_context",
    "PromptTemplate",
    "QuestionGenerationPrompt",
    "question_generation_prompt"
]