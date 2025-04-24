"""
QuizCraft
=========

A tool to extract and generate quiz questions from PDFs.

This package provides functionality to:
1. Extract text from PDF documents with OCR support

2. Segment text into logical sections
3. Extract existing questions from educational content

4. Generate new questions using the Claude API
5. Create interactive quizzes

Usage:
    >>> from quizcraft.pdf.extractor import PDFExtractor
    >>> extractor = PDFExtractor()
    >>> segments = extractor.extract_text("path/to/document.pdf")
"""

__version__ = "0.1.0"
