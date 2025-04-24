#!/usr/bin/env python3
"""
Test script for direct question extraction
"""

import os
import sys
from pathlib import Path
import re

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from quizcraft.questions.extractor import QuestionExtractor
from quizcraft.questions.models import Question


def test_option_extraction():
    """Test the option extraction specifically"""
    # Sample text with options
    sample_text = """
    1. What is Python?
    A) A snake
    B) A programming language
    C) A game
    D) A tool
    
    Answer: B
    """
    
    # Option patterns
    option_patterns = [
        # A) Option text or A. Option text
        r"^\s*([A-E])[\.\)]\s*(.+)$",
        # a) Option text or a. Option text
        r"^\s*([a-e])[\.\)]\s*(.+)$",
        # 1) Option text or 1. Option text (up to 5 options)
        r"^\s*([1-5])[\.\)]\s*(.+)$",
    ]
    
    options = {}
    option_matches = []
    
    # Try each option pattern
    for pattern in option_patterns:
        for line in sample_text.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                key, value = match.groups()
                print(f"Match found: key={key}, value={value}")
                # Standardize keys to uppercase
                key = key.upper()
                # Convert numeric keys to alphabetic (1->A, 2->B, etc.)
                if key.isdigit():
                    # Convert to 0-based index, then to ASCII (A=65)
                    key = chr(64 + int(key))
                option_matches.append((key, value.strip()))
    
    # Process all matches and handle potential duplicates
    for key, value in option_matches:
        options[key] = value
    
    print(f"Final options: {options}")


def test_question_extraction():
    """Test the question text extraction"""
    # Sample text
    sample_text = "1. What is Python?"
    
    # Question patterns
    question_patterns = [
        r"\b(?:(?:[0-9]+|[A-Z]|[a-z]|[IVX]+)[\.\)])\s+(.+\?)",  # Numbered questions
        r"\bQuestion\s+(?:[0-9]+|[A-Z])\s*[:\.]\s*(.+\?)",  # "Question X" format
        r"^(.+\?)\s*$",  # Any line ending with question mark
    ]
    
    # Try each pattern
    for pattern in question_patterns:
        match = re.search(pattern, sample_text)
        if match:
            question_text = match.group(1)
            print(f"Match found with pattern: {pattern}")
            print(f"Extracted question: {question_text}")


def main():
    """Test direct question extraction"""
    print("Testing option extraction:")
    test_option_extraction()
    
    print("\nTesting question extraction:")
    test_question_extraction()


if __name__ == "__main__":
    main()