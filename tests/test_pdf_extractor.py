"""
Tests for PDF extraction functionality
"""
import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quizcraft.pdf.extractor import PDFExtractor, segment_text


class TestPDFExtractor(unittest.TestCase):
    """Test cases for PDFExtractor class"""
    
    @patch('fitz.open')
    def test_extract_text_basic(self, mock_open):
        """Test basic text extraction without OCR"""
        # Mock PDF document
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample text for testing"
        mock_page.get_images.return_value = []
        mock_doc.__iter__.return_value = [mock_page]
        mock_open.return_value = mock_doc
        
        # Create extractor and extract text
        extractor = PDFExtractor(use_ocr_fallback=False)
        segments = extractor.extract_text("dummy.pdf")
        
        # Verify results
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["text"], "Sample text for testing")
        self.assertEqual(segments[0]["page"], 1)
        self.assertEqual(segments[0]["metadata"]["has_images"], False)
    
    def test_segment_text(self):
        """Test text segmentation functionality"""
        # Test input
        input_segments = [
            {
                "page": 1,
                "text": "Heading 1:\n\nThis is a paragraph.\n\nThis is another paragraph with a question?\n\n• Bullet point 1",
                "metadata": {"has_images": False, "has_tables": False}
            }
        ]
        
        # Segment text
        processed = segment_text(input_segments)
        
        # Verify results
        self.assertEqual(len(processed), 4)
        self.assertEqual(processed[0]["type"], "heading")
        self.assertEqual(processed[1]["type"], "paragraph")
        self.assertEqual(processed[2]["type"], "potential_question")
        self.assertEqual(processed[3]["type"], "bullet_point")


if __name__ == '__main__':
    unittest.main()