"""Anthropic Claude API client with error handling and retry logic."""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union

import anthropic
import requests
from anthropic.types import Message, MessageParam

from .credentials import get_api_key
from .tokens import estimate_token_count

logger = logging.getLogger(__name__)

# Constants
MAX_RETRIES = 3
BASE_RETRY_DELAY = 1  # seconds


class ClaudeClient:
    """Client for interacting with the Anthropic Claude API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the Claude client.
        
        Args:
            api_key: Optional API key. If not provided, will be retrieved from env.
            model: Claude model to use. Defaults to claude-3-haiku for cost efficiency.
        """
        self.api_key = api_key or get_api_key()
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a response from Claude.
        
        Args:
            prompt: The user prompt to send to Claude
            system_prompt: Optional system prompt to set context
            max_tokens: Maximum tokens in the response
            temperature: Controls randomness (0.0-1.0)
            top_p: Controls diversity via nucleus sampling
            stop_sequences: Optional list of sequences that will stop generation
            
        Returns:
            Dictionary containing the response and metadata
            
        Raises:
            ValueError: If the prompt is invalid
            RuntimeError: If API calls consistently fail
        """
        # Validate input parameters
        self._validate_input(prompt)
        
        # Prepare request parameters
        params = self._prepare_request_params(
            prompt, 
            system_prompt, 
            max_tokens, 
            temperature, 
            top_p, 
            stop_sequences
        )
        
        # Make API call with retry logic
        return self._make_api_call_with_retry(params)
    
    def _validate_input(self, prompt: str) -> None:
        """
        Validate input parameters.
        
        Args:
            prompt: The prompt to validate
            
        Raises:
            ValueError: If prompt is invalid
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Validate token count
        token_estimate = estimate_token_count(prompt)
        if token_estimate > 100000:  # Claude 3 models support up to 200K tokens
            logger.warning(f"Prompt is very large: ~{token_estimate} tokens")
    
    def _prepare_request_params(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
        top_p: float,
        stop_sequences: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Prepare request parameters for Claude API.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens in response
            temperature: Controls randomness
            top_p: Controls diversity
            stop_sequences: Optional sequences to stop generation
            
        Returns:
            Dictionary of request parameters
        """
        # Set up message parameters
        messages: List[MessageParam] = [
            {"role": "user", "content": prompt}
        ]
        
        # Configure request parameters
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "messages": messages,
        }
        
        # Add system prompt if provided
        if system_prompt:
            params["system"] = system_prompt
            
        # Add stop sequences if provided
        if stop_sequences:
            params["stop_sequences"] = stop_sequences
            
        # Log the request parameters for debugging
        logger.debug(f"Request parameters: {params}")
        
        return params
    
    def _make_api_call_with_retry(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API call with exponential backoff retry logic.
        
        Args:
            params: Request parameters for Claude API
            
        Returns:
            Response dictionary
            
        Raises:
            RuntimeError: If API calls consistently fail
        """
        for attempt in range(MAX_RETRIES):
            try:
                return self._execute_api_call(params)
            except anthropic.RateLimitError as e:
                self._handle_rate_limit_error(attempt, e)
            except anthropic.APIError as e:
                if not self._handle_api_error(attempt, e):
                    break
            except requests.exceptions.RequestException as e:
                if not self._handle_network_error(attempt, e):
                    break
        
        # If we get here, all retries failed
        raise RuntimeError(f"Failed to generate response after {MAX_RETRIES} attempts")
    
    def _execute_api_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single API call and format the response.
        
        Args:
            params: Request parameters
            
        Returns:
            Formatted response dictionary
        """
        response = self.client.messages.create(**params)
        
        # Extract and return relevant information
        return {
            "content": response.content[0].text,
            "model": response.model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "id": response.id
        }
    
    def _calculate_delay(self, attempt: int, jitter: float = 0.1) -> float:
        """
        Calculate delay with exponential backoff and jitter.
        
        Args:
            attempt: Current attempt number (0-based)
            jitter: Random jitter factor to add
            
        Returns:
            Delay in seconds
        """
        return BASE_RETRY_DELAY * (2 ** attempt) + (jitter * attempt)
    
    def _handle_rate_limit_error(self, attempt: int, error: Exception) -> None:
        """
        Handle rate limit errors with appropriate backoff.
        
        Args:
            attempt: Current attempt number (0-based)
            error: The exception that occurred
        """
        delay = self._calculate_delay(attempt)
        logger.warning(f"Rate limit hit. Retrying in {delay:.1f}s. Error: {str(error)}")
        time.sleep(delay)
    
    def _handle_api_error(self, attempt: int, error: Exception) -> bool:
        """
        Handle API errors with appropriate backoff.
        
        Args:
            attempt: Current attempt number (0-based)
            error: The exception that occurred
            
        Returns:
            True if retry should continue, False otherwise
        """
        if attempt < MAX_RETRIES - 1:
            delay = self._calculate_delay(attempt)
            logger.warning(f"API error: {str(error)}. Retrying in {delay:.1f}s.")
            time.sleep(delay)
            return True
        else:
            logger.error(f"API error after {MAX_RETRIES} attempts: {str(error)}")
            raise RuntimeError(f"Failed to generate response after {MAX_RETRIES} attempts") from error
    
    def _handle_network_error(self, attempt: int, error: Exception) -> bool:
        """
        Handle network errors with appropriate backoff.
        
        Args:
            attempt: Current attempt number (0-based)
            error: The exception that occurred
            
        Returns:
            True if retry should continue, False otherwise
        """
        if attempt < MAX_RETRIES - 1:
            delay = self._calculate_delay(attempt)
            logger.warning(f"Network error: {str(error)}. Retrying in {delay:.1f}s.")
            time.sleep(delay)
            return True
        else:
            logger.error(f"Network error after {MAX_RETRIES} attempts: {str(error)}")
            raise RuntimeError(f"Network error after {MAX_RETRIES} attempts") from error
    
    def validate_and_fix_json_response(self, content: str) -> Dict[str, Any]:
        """
        Validate and attempt to fix malformed JSON in Claude's response.
        
        Args:
            content: Response content from Claude API
            
        Returns:
            Parsed JSON as a dictionary
            
        Raises:
            ValueError: If JSON cannot be parsed after repair attempts
        """
        # First try to parse directly
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON if embedded in text
        try:
            # Look for JSON between triple backticks
            if "```json" in content and "```" in content.split("```json", 1)[1]:
                json_content = content.split("```json", 1)[1].split("```", 1)[0].strip()
                return json.loads(json_content)
            
            # Look for JSON between regular backticks
            if "```" in content:
                blocks = content.split("```")
                for block in blocks:
                    if block.strip() and block.strip()[0] == "{" and block.strip()[-1] == "}":
                        return json.loads(block.strip())
            
            # Look for content that starts with { and ends with }
            import re
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
                
        except (json.JSONDecodeError, IndexError):
            pass
        
        # If all attempts fail, raise an error
        raise ValueError("Failed to parse response as valid JSON")