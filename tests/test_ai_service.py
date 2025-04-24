"""Tests for the AI service module."""

import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import json

from quizcraft.ai.service import AIService


class AIServiceTest(unittest.TestCase):
    """Test the AI service."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for cache
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_path = os.path.join(self.temp_dir.name, "cache.db")
        
        # Create env vars for testing
        os.environ["ANTHROPIC_API_KEY"] = "test_api_key"
        os.environ["CACHE_DB_PATH"] = self.cache_path
        
    def tearDown(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()
        
    @patch('quizcraft.ai.service.ClaudeClient')
    @patch('quizcraft.ai.service.ResponseCache')
    def test_generate_questions(self, mock_cache, mock_client_class):
        """Test that question generation produces valid JSON."""
        # Mock the client and cache
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Setup mock response
        mock_response = {
            "content": """```json
{
  "questions": [
    {
      "question": "Test question?",
      "options": {
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      },
      "correct_answer": "A",
      "explanation": "Test explanation"
    }
  ]
}
```""",
            "usage": {"input_tokens": 100, "output_tokens": 50},
            "model": "claude-3-haiku-20240307"
        }
        mock_client.generate_response.return_value = mock_response
        
        # Mock the JSON validation to return expected format
        mock_client.validate_and_fix_json_response.return_value = {
            "questions": [
                {
                    "question": "Test question?",
                    "options": {
                        "A": "Option A",
                        "B": "Option B",
                        "C": "Option C",
                        "D": "Option D"
                    },
                    "correct_answer": "A",
                    "explanation": "Test explanation"
                }
            ]
        }
        
        # Mock cache to return None (no cache hit)
        mock_cache_instance = MagicMock()
        mock_cache.return_value = mock_cache_instance
        mock_cache_instance.get.return_value = None
        
        # Create service and generate questions
        service = AIService()
        result = service.generate_questions(context="Test context", num_questions=1)
        
        # Validate result
        self.assertIn("questions", result["questions"])
        self.assertEqual(len(result["questions"]["questions"]), 1)
        self.assertEqual(result["questions"]["questions"][0]["question"], "Test question?")
        self.assertEqual(result["token_usage"]["input_tokens"], 100)
        self.assertEqual(result["token_usage"]["output_tokens"], 50)
        self.assertFalse(result["from_cache"])
        
    @patch('quizcraft.ai.service.ClaudeClient')
    @patch('quizcraft.ai.service.ResponseCache')
    def test_cached_response(self, mock_cache, mock_client_class):
        """Test that cached responses are properly returned."""
        # Mock the client and cache
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Setup mock cached response
        mock_cached_response = {
            "content": '{"questions": [{"question": "Cached question?"}]}',
            "usage": {"input_tokens": 50, "output_tokens": 25},
            "model": "claude-3-haiku-20240307"
        }
        
        # Mock cache to return a cached response
        mock_cache_instance = MagicMock()
        mock_cache.return_value = mock_cache_instance
        mock_cache_instance.get.return_value = mock_cached_response
        
        # Client should validate and fix the JSON
        mock_client.validate_and_fix_json_response.return_value = {
            "questions": [{"question": "Cached question?"}]
        }
        
        # Create service and generate questions
        service = AIService()
        result = service.generate_questions(context="Test context", num_questions=1)
        
        # Validate result
        self.assertEqual(result["questions"]["questions"][0]["question"], "Cached question?")
        self.assertEqual(result["token_usage"]["input_tokens"], 50)
        self.assertEqual(result["token_usage"]["output_tokens"], 25)
        self.assertTrue(result["from_cache"])
        
        # Verify no API call was made
        mock_client.generate_response.assert_not_called()


if __name__ == "__main__":
    unittest.main()