"""
Text processing utilities for QuizCraft
"""
from typing import List, Dict, Any, Optional
import re


def split_into_chunks(text: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Split text into logical chunks respecting paragraph boundaries
    
    Args:
        text: Text to split
        max_chunk_size: Maximum characters per chunk
        
    Returns:
        List of text chunks
    """
    # Split text by paragraphs
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed max size, start a new chunk
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens for Claude API
    
    Args:
        text: Text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    # Rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4


def extract_metadata(text: str) -> Dict[str, Any]:
    """
    Extract metadata from text to enhance question generation
    
    Args:
        text: Text to extract metadata from
        
    Returns:
        Dictionary of metadata
    """
    metadata = {
        "has_numbers": bool(re.search(r'\d+', text)),
        "has_lists": bool(re.search(r'(\n\s*[-•*]\s+)', text)),
        "word_count": len(text.split()),
    }
    
    return metadata