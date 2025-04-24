"""
Tests for utility functions
"""
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quizcraft.utils.text import split_into_chunks, estimate_tokens, extract_metadata


class TestTextUtils(unittest.TestCase):
    """Test cases for text utility functions"""
    
    def test_split_into_chunks(self):
        """Test splitting text into chunks"""
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3.\n\nParagraph 4."
        chunks = split_into_chunks(text, max_chunk_size=30)
        
        # Should split into at least 2 chunks
        self.assertGreater(len(chunks), 1)
        
        # Each chunk should be under the max size
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 30)
    
    def test_estimate_tokens(self):
        """Test token estimation"""
        text = "This is a sample text for testing token estimation."
        tokens = estimate_tokens(text)
        
        # Should be approximately characters / 4
        self.assertAlmostEqual(tokens, len(text) // 4, delta=1)
    
    def test_extract_metadata(self):
        """Test metadata extraction"""
        text = "This is a test.\n\n• Item 1\n• Item 2\n\nHere are some numbers: 123, 456."
        metadata = extract_metadata(text)
        
        # Should detect numbers and lists
        self.assertTrue(metadata["has_numbers"])
        self.assertTrue(metadata["has_lists"])
        self.assertGreater(metadata["word_count"], 0)


if __name__ == '__main__':
    unittest.main()